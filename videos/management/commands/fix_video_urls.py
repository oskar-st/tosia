from django.core.management.base import BaseCommand
from videos.models import Video
import re

class Command(BaseCommand):
    help = 'Fixes YouTube URLs for existing videos to ensure thumbnails work'

    def handle(self, *args, **kwargs):
        videos = Video.objects.all()
        fixed_count = 0

        for video in videos:
            # Convert various YouTube URL formats to standard format
            patterns = [
                (r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?]+)', lambda m: f'https://www.youtube.com/watch?v={m.group(1)}'),
                (r'(?:youtube\.com\/embed\/)([^&\n?]+)', lambda m: f'https://www.youtube.com/watch?v={m.group(1)}'),
                (r'(?:youtube\.com\/v\/)([^&\n?]+)', lambda m: f'https://www.youtube.com/watch?v={m.group(1)}'),
                (r'(?:youtube\.com\/watch\?.*&v=)([^&\n?]+)', lambda m: f'https://www.youtube.com/watch?v={m.group(1)}'),
            ]
            
            original_url = video.youtube_url
            for pattern, replacement in patterns:
                match = re.search(pattern, original_url)
                if match:
                    new_url = replacement(match)
                    if new_url != original_url:
                        video.youtube_url = new_url
                        video.save()
                        fixed_count += 1
                        self.stdout.write(f'Fixed URL for video "{video.title}": {original_url} -> {new_url}')
                    break

        self.stdout.write(self.style.SUCCESS(f'Successfully fixed {fixed_count} video URLs')) 