from django.shortcuts import render, redirect, get_object_or_404
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
            return redirect('blog:blog_list')
    return render(request, 'blog/add_post.html')

@login_required
def delete_post(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    if request.user == post.author or request.user.is_staff:
        post.delete()
        messages.success(request, _('Blog post deleted successfully!'))
    return redirect('blog:blog_list')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, _('You do not have permission to edit this post.'))
        return redirect('blog:blog_list')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            post.title = title
            post.content = content
            post.save()
            messages.success(request, _('Blog post updated successfully!'))
            return redirect('blog:blog_list')
    
    return render(request, 'blog/edit_post.html', {'post': post})
