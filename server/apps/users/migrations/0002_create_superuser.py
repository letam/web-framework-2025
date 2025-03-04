# Generated by Django 5.1.5 on 2025-02-25 04:11

from django.db import migrations
from django.contrib.auth import get_user_model


def create_superuser(apps, schema_editor):
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            password="admin"
        )


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
