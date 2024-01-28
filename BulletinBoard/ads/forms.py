from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post, Comment
from ckeditor.fields import RichTextField
from embed_video.fields import EmbedVideoFormField
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model


class PostForm(forms.ModelForm):
    content = RichTextField()

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'photo1', 'photo2', 'video1', 'video2',
                  'media_url', 'video_url', 'media']


class PostEditForm(forms.ModelForm):
    content = RichTextField()

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'photo1', 'photo2', 'video1', 'video2',
                  'media_url', 'video_url', 'media']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=30, label='Username')
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.username = self.cleaned_data.get('username', '')
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

