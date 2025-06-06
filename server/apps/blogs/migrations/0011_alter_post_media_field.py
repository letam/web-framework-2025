# Generated by Django 5.1.5 on 2025-05-20 21:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0010_create_media_records'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='media_mp3',
        ),
        migrations.RemoveField(
            model_name='post',
            name='media_s3_file_key',
        ),
        migrations.RemoveField(
            model_name='post',
            name='media_type',
        ),
        migrations.RemoveField(
            model_name='post',
            name='media',
        ),
        migrations.AddField(
            model_name='post',
            name='media',
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='blogs.media',
            ),
        ),
    ]
