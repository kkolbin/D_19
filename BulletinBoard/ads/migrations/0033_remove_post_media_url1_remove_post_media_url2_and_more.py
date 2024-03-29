# Generated by Django 4.2.9 on 2024-01-27 17:22

from django.db import migrations, models
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0032_remove_post_media_remove_post_media_url_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='media_url1',
        ),
        migrations.RemoveField(
            model_name='post',
            name='media_url2',
        ),
        migrations.RemoveField(
            model_name='post',
            name='video_url1',
        ),
        migrations.RemoveField(
            model_name='post',
            name='video_url2',
        ),
        migrations.AddField(
            model_name='post',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='post_media/'),
        ),
        migrations.AddField(
            model_name='post',
            name='media_url',
            field=models.URLField(default='https://default-media-url.com'),
        ),
        migrations.AddField(
            model_name='post',
            name='photo1',
            field=models.ImageField(blank=True, null=True, upload_to='post_photos/'),
        ),
        migrations.AddField(
            model_name='post',
            name='photo2',
            field=models.ImageField(blank=True, null=True, upload_to='post_photos/'),
        ),
        migrations.AddField(
            model_name='post',
            name='video1',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='video2',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='video_url',
            field=models.URLField(blank=True, null=True, verbose_name='Video URL'),
        ),
    ]
