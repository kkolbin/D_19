# Generated by Django 5.0 on 2024-01-03 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0003_rename_media_file_post_media'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='video_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
