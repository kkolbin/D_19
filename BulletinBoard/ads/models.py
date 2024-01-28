from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from embed_video.fields import EmbedVideoField
from django.conf import settings


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('Танки', 'Танки'),
        ('Хилы', 'Хилы'),
        ('ДД', 'ДД'),
        ('Торговцы', 'Торговцы'),
        ('Гилдмастеры', 'Гилдмастеры'),
        ('Квестгиверы', 'Квестгиверы'),
        ('Кузнецы', 'Кузнецы'),
        ('Кожевники', 'Кожевники'),
        ('Зельевары', 'Зельевары'),
        ('Мастера заклинаний', 'Мастера заклинаний'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_posts', default=1)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = RichTextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Танки')
    created_at = models.DateTimeField(default=timezone.now)
    photo1 = models.ImageField(upload_to='post_photos/', null=True, blank=True)
    photo2 = models.ImageField(upload_to='post_photos/', null=True, blank=True)
    video1 = EmbedVideoField(null=True, blank=True)
    video2 = EmbedVideoField(null=True, blank=True)
    media_url = models.URLField(default='https://default-media-url.com')
    video_url = models.URLField(verbose_name='Video URL', blank=True, null=True)
    media = models.FileField(upload_to='post_media/', null=True, blank=True)
    comments = models.ManyToManyField('Comment', related_name='post_comments')

    def get_media_urls(self):
        return [self.media_url1, self.media_url2]

    def get_video_urls(self):
        return [self.video_url1, self.video_url2]

    def get_comments(self):
        return self.comments.all()

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_comments')
    content = models.TextField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'


class DailyNewsletter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_sent = models.DateField()
    posts = models.ManyToManyField(Post)

    def __str__(self):
        return f'{self.user.username} - {self.date_sent}'

