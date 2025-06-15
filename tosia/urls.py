from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponse

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    ]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('blog/', include('blog.urls')),
    path('users/', include('users.urls')),
    path('videos/', include('videos.urls')),
    prefix_default_language=True,
)
