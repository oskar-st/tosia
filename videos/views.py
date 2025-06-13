from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django import forms
from .models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'youtube_url']

def is_admin(user):
    return user.is_authenticated and user.is_admin

@login_required
@user_passes_test(is_admin)
def videos_list(request):
    videos = Video.objects.all()
    return render(request, 'videos/videos_list.html', {'videos': videos})

@login_required
@user_passes_test(is_admin)
def video_create(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('videos:videos_list')
    else:
        form = VideoForm()
    return render(request, 'videos/video_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def video_update(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        form = VideoForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            return redirect('videos:videos_list')
    else:
        form = VideoForm(instance=video)
    return render(request, 'videos/video_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        video.delete()
        return redirect('videos:videos_list')
    return render(request, 'videos/video_confirm_delete.html', {'video': video})
