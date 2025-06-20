from django.shortcuts import render
from django.utils import translation
from blog.models import BlogPost
from videos.models import Video
from django.db.models import Q

def home(request):
    current_lang = translation.get_language()
    print("Current session lang:", current_lang)
    return render(request, 'main/home.html', {
        'current_lang': current_lang
    })

def search(request):
    query = request.GET.get('q', '').strip()
    user = request.user
    results = []

    if query:
        # Blogs
        blog_qs = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        if not (user.is_authenticated and user.is_staff):
            blog_qs = blog_qs.filter(is_public=True)
        for b in blog_qs:
            results.append({'type': 'Blog', 'title': b.title, 'url': f"/blog/?highlight={b.id}#highlighted-post"})

        # Videos
        video_qs = Video.objects.filter(
            Q(title__icontains=query)
        )
        if not (user.is_authenticated and user.is_staff):
            video_qs = video_qs.filter(is_public=True)
        for v in video_qs:
            results.append({'type': 'Video', 'title': v.title, 'url': v.youtube_url})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'main/search_results_partial.html', {'results': results, 'query': query})
    return render(request, 'main/search_results.html', {'results': results, 'query': query})