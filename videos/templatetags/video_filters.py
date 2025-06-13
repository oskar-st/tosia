from django import template
import re

register = template.Library()

@register.filter
def youtube_id(url):
    """Extract YouTube video ID from URL."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?]+)',  # Standard URLs
        r'(?:youtube\.com\/embed\/)([^&\n?]+)',  # Embed URLs
        r'(?:youtube\.com\/v\/)([^&\n?]+)',  # Old format URLs
        r'(?:youtube\.com\/watch\?.*&v=)([^&\n?]+)',  # URLs with other parameters
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None 