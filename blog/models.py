from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
