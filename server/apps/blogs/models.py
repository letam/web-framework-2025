from django.conf import settings
from django.db import models


class Post(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    head = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    audio = models.FileField(upload_to='audio/', blank=True, null=True)
    parent = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.head
