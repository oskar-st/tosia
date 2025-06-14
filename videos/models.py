from django.db import models
from django.utils import timezone
import re

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    youtube_url = models.URLField()
    created_at = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def youtube_id(self):
        """Get YouTube video ID as a property for template use."""
        return self.get_youtube_id()

    @property
    def thumbnail_url(self):
        # Extract video ID from various YouTube URL formats
        video_id = None
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/|youtube\.com\/watch\?.*&v=)([^&\n?]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.youtube_url)
            if match:
                video_id = match.group(1)
                break
        
        if video_id:
            return f'https://img.youtube.com/vi/{video_id}/mqdefault.jpg'
        return None

    def get_youtube_id(self):
        """Extract YouTube video ID from URL."""
        print(f"Getting YouTube ID for URL: {self.youtube_url}")  # Debug output
        # Handle various YouTube URL formats
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?]+)',  # Standard URLs
            r'(?:youtube\.com\/embed\/)([^&\n?]+)',  # Embed URLs
            r'(?:youtube\.com\/v\/)([^&\n?]+)',  # Old format URLs
            r'(?:youtube\.com\/watch\?.*&v=)([^&\n?]+)',  # URLs with other parameters
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.youtube_url)
            if match:
                video_id = match.group(1)
                print(f"Found video ID: {video_id}")  # Debug output
                return video_id
        print("No video ID found")  # Debug output
        return None

    def get_thumbnail_url(self):
        """Get YouTube thumbnail URL."""
        video_id = self.get_youtube_id()
        if video_id:
            thumbnail_url = f'https://img.youtube.com/vi/{video_id}/mqdefault.jpg'
            print(f"Generated thumbnail URL: {thumbnail_url}")  # Debug output
            return thumbnail_url
        print("No thumbnail URL generated")  # Debug output
        return None
