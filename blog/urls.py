from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('add/', views.add_post, name='add_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
] 