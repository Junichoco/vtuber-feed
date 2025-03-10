from django.core.management.base import BaseCommand

import feedparser
from dateutil import parser

from feed.models import Video

class Command(BaseCommand):
    def handle(self, *args, **options):
        feed = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCtuoyOZhnxJ12pE294FdH8Q")
        # print(feed)
        print(feed.entries[0])
        # if feed.entries:
        #     for entry in feed.entries:

        #         video = Video(
        #             title = entry.title
        #             channel = entry.author
        #             pub_date = entry.published
        #             link = entry.link
        #             image = entry.media_thumbnail[0]['url']
        #         )
        #         # print(f"Title: {entry.title}")
        #         # print(f"Link: {entry.link}")
        #         # print(f"Published: {entry.published}")
        #         # print(f"Channel: {entry.author}")
        #         # print(f"Thumbnail: {entry.media_thumbnail[0]['url']}")
        #         # print("-" * 20)
        # else:
        #     print("No entries found in the feed.")
