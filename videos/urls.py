from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.videos_list, name='videos_list'),
    path('new/', views.video_create, name='video_create'),
    path('<int:pk>/edit/', views.video_update, name='video_update'),
    path('<int:pk>/delete/', views.video_delete, name='video_delete'),
] 