from videos.models import Video
from blog.models import BlogPost

def public_content(request):
    has_public_videos = Video.objects.filter(is_public=True).exists()
    has_public_posts = BlogPost.objects.filter(is_public=True).exists()
    print(f"Context processor - has_public_videos: {has_public_videos}, has_public_posts: {has_public_posts}")
    return {
        'has_public_videos': has_public_videos,
        'has_public_posts': has_public_posts,
    } 