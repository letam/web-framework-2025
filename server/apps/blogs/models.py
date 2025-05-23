from django.conf import settings
from django.db import models
import os.path
import os

import logging

from .utils import convert_to_mp3

# Configure logging
logger = logging.getLogger('server.apps.blogs')


def media_file_path(instance, filename):
    return f'post/{instance.id}/media/{filename}'


MEDIA_TYPE_CHOICES = [
    ('audio', 'Audio'),
    ('video', 'Video'),
]


class Media(models.Model):
    file = models.FileField(upload_to=media_file_path)
    mp3_file = models.FileField(upload_to=media_file_path, blank=True)
    s3_file_key = models.CharField(max_length=255, blank=True)
    media_type = models.CharField(max_length=255, choices=MEDIA_TYPE_CHOICES)
    duration = models.DurationField(null=True, blank=True)  # For storing media duration
    thumbnail = models.ImageField(upload_to=media_file_path, blank=True)  # For storing thumbnail
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # If this is a new record
        if self.id is None:
            # Store the media file temporarily
            file = self.file
            self.file = None

            # First save the record without file, so that we can get an id for media_file_path
            super().save(*args, **kwargs)

            # Set file before re-saving
            self.file = file
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super().save(*args, **kwargs)

    def convert_to_mp3(self):
        """Convert the media file to MP3 format."""
        if not self.file.path.endswith('.mp3'):
            convert_to_mp3(self.file.path)
            new_media_file_name = os.path.splitext(self.file.name)[0] + '.mp3'
            self.mp3_file = new_media_file_name
            self.save()


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    head = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    media = models.OneToOneField(Media, on_delete=models.SET_NULL, null=True, blank=True)
    parent = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.head

    def save(self, *args, **kwargs):
        # If this is a new post
        if self.id is None:
            # Strip media file from the post--it will be used in separate new Media record
            media_file = self.media
            self.media = None

            # First save the post without media
            super().save(*args, **kwargs)

            # If there was a media file, create a new Media record
            if media_file:
                media = Media(
                    file=media_file,
                    media_type=self.media_type if hasattr(self, 'media_type') else 'audio',
                )
                media.save()
                self.media = media
                super().save(update_fields=['media'])
        else:
            super().save(*args, **kwargs)
