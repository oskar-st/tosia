from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

from blog.views import toggle_public

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('blog/', include('blog.urls')),
    path('videos/', include('videos.urls')),
    path('users/', include('users.urls')),
    path('toggle-post-visibility/<int:post_id>/', toggle_public, name='toggle_post_visibility'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('blog/', include('blog.urls')),
    path('videos/', include('videos.urls')),
    path('users/', include('users.urls')),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
