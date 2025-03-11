from django.core.management.base import BaseCommand

import feedparser
from dateutil import parser

from feed.models import Video

import logging
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)

def save_new_episodes(feed):
    if feed.entries:
        for entry in feed.entries:
            if not Video.objects.filter(link=entry.link).exists():
                video = Video(
                    title = entry.title,
                    channel = entry.author,
                    pub_date = entry.published,
                    link = entry.link,
                    image = entry.media_thumbnail[0]['url'],
                )
                video.save()

def fetch_raki_videos():
    _feed = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCtuoyOZhnxJ12pE294FdH8Q")
    save_new_episodes(_feed)

def fetch_ami_videos():
    _feed = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCkjP_w607B-n4kWJrZAsHMQ")
    save_new_episodes(_feed)

def fetch_ito_videos():
    _feed = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCi9O6GC9DvnrXqQfgXrNaYg")
    save_new_episodes(_feed)

def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            fetch_raki_videos,
            trigger="interval",
            minutes=2,
            id="Raki",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Raki Videos.")

        scheduler.add_job(
            fetch_ami_videos,
            trigger="interval",
            minutes=2,
            id="Ami videos",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Ami Videos.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="Delete Old Job Executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: Delete Old Job Executions.")

        scheduler.add_job(
            fetch_ito_videos,
            trigger="interval",
            minutes=2,
            id="Ito videos",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Ito Videos.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
