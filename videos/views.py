from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Video
import re
from django.contrib.admin.views.decorators import staff_member_required


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

def videos_list(request):
    if request.user.is_staff:
        videos = Video.objects.all().order_by('id')  # ordering fixed
    else:
        videos = Video.objects.filter(is_public=True).order_by('id')
    return render(request, 'videos/video_list.html', {'videos': videos})

@login_required
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
def video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        video.delete()
        return redirect('videos:videos_list')
    return render(request, 'videos/video_confirm_delete.html', {'video': video})

@staff_member_required
def video_toggle_public(request, pk):
    video = get_object_or_404(Video, pk=pk)
    video.is_public = not video.is_public
    video.save()
    return redirect('videos:videos_list')
