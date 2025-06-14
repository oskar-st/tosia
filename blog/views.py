from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BlogPost
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

def blog_list(request):
    if request.user.is_staff:
        posts = BlogPost.objects.all()
    else:
        posts = BlogPost.objects.filter(is_public=True)
    return render(request, 'blog/blog_list.html', {'posts': posts})

@login_required
def add_post(request):
    if request.user.is_staff:
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            if title and content:
                BlogPost.objects.create(title=title, content=content, author=request.user)
                messages.success(request, _('Blog post created successfully!'))
                return redirect('blog:blog_list')
            else:
                messages.error(request, _('Both title and content are required.'))
        return render(request, 'blog/add_post.html')
    else:
        messages.error(request, _('You do not have permission to add posts.'))
        return redirect('blog:blog_list')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.user.is_staff:
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            if title and content:
                post.title = title
                post.content = content
                post.save()
                messages.success(request, _('Blog post updated successfully!'))
                return redirect('blog:blog_list')
            else:
                messages.error(request, _('Both title and content are required.'))
        return render(request, 'blog/edit_post.html', {'post': post})
    else:
        messages.error(request, _('You do not have permission to edit posts.'))
        return redirect('blog:blog_list')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.user.is_staff:
        if request.method == 'POST':
            post.delete()
            messages.success(request, _('Blog post deleted successfully!'))
            return redirect('blog:blog_list')
        return render(request, 'blog/blog_confirm_delete.html', {'post': post})
    else:
        messages.error(request, _('You do not have permission to delete posts.'))
        return redirect('blog:blog_list')

@staff_member_required
def toggle_public(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    post.is_public = not post.is_public
    post.save()
    return redirect('blog:blog_list')
