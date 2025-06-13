from django.core.management.base import BaseCommand
from videos.models import Video

class Command(BaseCommand):
    help = 'Test thumbnail URL generation for all videos'

    def handle(self, *args, **options):
        videos = Video.objects.all()
        for video in videos:
            self.stdout.write(f"\nVideo: {video.title}")
            self.stdout.write(f"URL: {video.youtube_url}")
            self.stdout.write(f"Video ID: {video.get_youtube_id()}")
            self.stdout.write(f"Thumbnail URL: {video.get_thumbnail_url()}") 