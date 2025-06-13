from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BlogPost
from django.utils.translation import gettext_lazy as _

# Create your views here.

def blog_home(request):
    return render(request, 'blog/blog_home.html')

def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog/blog_list.html', {'posts': posts})

@login_required
def add_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            BlogPost.objects.create(
                title=title,
                content=content,
                author=request.user
            )
            messages.success(request, _('Blog post created successfully!'))
            return redirect('blog_list')
    return render(request, 'blog/add_post.html')

@login_required
def delete_post(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    if request.user == post.author or request.user.is_staff:
        post.delete()
        messages.success(request, _('Blog post deleted successfully!'))
    return redirect('blog_list')
