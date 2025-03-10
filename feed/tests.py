from django.test import TestCase

# Create your tests here.
from django.utils import timezone
from .models import Video
from django.urls.base import reverse
from datetime import datetime

class FeedTests(TestCase):
    def setUp(self):
        self.video = Video.objects.create(
            title="Guerilla Karaoke",
            description="Tonight, we shall dance in the depths of the Netherworld.",
            pub_date=timezone.now(),
            link="https://vtuber-list-941da732d306.herokuapp.com/home",
            image="https://image.myawesomeshow.com",
            channel="My Channel",
            guid="de194720-7b4c-49e2-a05f-432436d3fetr",
        )

    def test_video_content(self):
        self.assertEqual(self.video.description, "Tonight, we shall dance in the depths of the Netherworld.")
        self.assertEqual(self.video.link, "https://vtuber-list-941da732d306.herokuapp.com/home")
        self.assertEqual(
            self.video.guid, "de194720-7b4c-49e2-a05f-432436d3fetr"
        )

    # def test_video_str_representation(self):
    #     self.assertEqual(
    #         str(self.video), "My Python Podcast: My Awesome Podcast Episode"
    #     )

    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse("homepage"))
        self.assertTemplateUsed(response, "homepage.html")
