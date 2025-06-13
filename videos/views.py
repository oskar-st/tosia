from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django import forms
from .models import Video
import re


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'youtube_url']
        widgets = {
            'youtube_url': forms.URLInput(attrs={'placeholder': 'https://www.youtube.com/watch?v=VIDEO_ID'})
        }

    def clean_youtube_url(self):
        url = self.cleaned_data['youtube_url']
        # Convert various YouTube URL formats to standard format
        patterns = [
            (r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?]+)', lambda m: f'https://www.youtube.com/watch?v={m.group(1)}'),
            (r'(?:youtube\.com\/embed\/)([^&\n?]+)', lambda m: f'https://www.youtube.com/watch?v={m.group(1)}'),
            (r'(?:youtube\.com\/v\/)([^&\n?]+)', lambda m: f'https://www.youtube.com/watch?v={m.group(1)}'),
            (r'(?:youtube\.com\/watch\?.*&v=)([^&\n?]+)', lambda m: f'https://www.youtube.com/watch?v={m.group(1)}'),
        ]
        
        for pattern, replacement in patterns:
            match = re.search(pattern, url)
            if match:
                return replacement(match)
        
        raise forms.ValidationError('Please enter a valid YouTube URL')

def is_admin(user):
    return user.is_authenticated and user.is_admin

@login_required
@user_passes_test(is_admin)
def videos_list(request):
    videos = Video.objects.all()
    # Prepare thumbnail URLs for each video
    for video in videos:
        video_id = None
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?]+)',  # Standard URLs
            r'(?:youtube\.com\/embed\/)([^&\n?]+)',  # Embed URLs
            r'(?:youtube\.com\/v\/)([^&\n?]+)',  # Old format URLs
            r'(?:youtube\.com\/watch\?.*&v=)([^&\n?]+)',  # URLs with other parameters
        ]
        
        for pattern in patterns:
            match = re.search(pattern, video.youtube_url)
            if match:
                video_id = match.group(1)
                break
        
        if video_id:
            video.thumbnail_url = f'https://img.youtube.com/vi/{video_id}/mqdefault.jpg'
        else:
            video.thumbnail_url = None
    
    return render(request, 'videos/video_list.html', {'videos': videos})

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
