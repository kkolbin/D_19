from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import PostForm, PostEditForm, CommentForm
from .models import Post, Comment, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import DetailView
from django.urls import reverse
from django.views.generic import ListView
from django.views import View
from django.shortcuts import render, redirect
import os
import requests
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.db.models import Count
from django.core.mail import send_mail


class HomeView(ListView):
    model = Post
    template_name = 'ads/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    extra_context = {'top_posts': Post.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')[:5]}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


def posts(request):
    # Логика для получения списка объявлений
    return render(request, 'ads/posts.html', {'posts': your_posts_data})


@login_required
def profile_view(request, username):
    user = User.objects.get(username=username)
    posts = user.posts.all()
    return render(request, 'ads/profile.html', {'user': user, 'posts': posts})


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostForm
    template_name = 'ads/create_post.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            media_url = form.cleaned_data.get('media_url')
            if media_url:
                media_path = os.path.join('media', str(post.pk))  # Modify the path accordingly
                os.makedirs(media_path, exist_ok=True)

                media_file_path = os.path.join(media_path, 'media_file.jpg')  # Modify the path accordingly
                success = fetch_and_save_media(media_url, media_file_path)
                if success:
                    post.media.name = os.path.relpath(media_file_path, 'media')
                    post.save()
                    messages.success(request, 'Media successfully fetched and saved.')
                else:
                    messages.error(request, 'Failed to fetch or save media. Please check the URL.')
            else:
                messages.warning(request, 'No media URL provided.')

            return redirect('ads:post_detail', pk=post.pk)
        return render(request, self.template_name, {'form': form})


def fetch_and_save_media(url, target_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        with open(target_path, 'wb') as f:
            f.write(response.content)
        return True
    except requests.RequestException as e:
        print(f"Error fetching media: {e}")
        return False


class PostDetailView(View):
    template_name = 'ads/post_detail.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post, is_accepted=True)
        form = CommentForm()
        category_url = reverse('ads:category_posts', args=[post.category])
        return render(request, self.template_name, {'post': post, 'comments': comments,
                                                    'form': form, 'category_url': category_url})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

            # Обновляем комментарии после сохранения нового комментария
            comments = Comment.objects.filter(post=post, is_accepted=True)
            form = CommentForm()
            return render(request, self.template_name, {'post': post, 'comments': comments, 'form': form})

        # Если форма недействительна, возвращаем старые комментарии
        comments = Comment.objects.filter(post=post, is_accepted=True)
        form = CommentForm()
        category_url = reverse('ads:category_posts', args=[post.category])

        return render(request, self.template_name,
                      {'post': post, 'comments': comments, 'form': form, 'category_url': category_url})


class PostEditView(LoginRequiredMixin, View):
    template_name = 'ads/edit_post.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk, user=request.user)
        form = PostEditForm(instance=post)
        return render(request, self.template_name, {'form': form, 'post': post})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk, user=request.user)
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            media_url = request.POST.get('media_url')
            if media_url:
                media_path = os.path.join('media', str(post.pk))  # Modify the path accordingly
                os.makedirs(media_path, exist_ok=True)

                media_file_path = os.path.join(media_path, 'media_file.jpg')  # Modify the path accordingly
                success = fetch_and_save_media(media_url, media_file_path)
                if success:
                    post.media.name = os.path.relpath(media_file_path, 'media')
                    post.save()

            return redirect('ads:post_detail', pk=post.pk)
        return render(request, self.template_name, {'form': form})


class AuthorProfileView(View):
    template_name = 'ads/author_profile.html'

    def get(self, request, username):
        author = get_object_or_404(User, username=username)
        posts = Post.objects.filter(author=author)
        return render(request, self.template_name, {'author': author, 'posts': posts})


class CategoryPostsView(View):
    template_name = 'ads/category_posts.html'

    def get(self, request, category):
        posts = Post.objects.filter(category=category)
        return render(request, self.template_name, {'category': category, 'posts': posts})


def create_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

            # Отправка email
            send_mail(
                'Уведомление о новом отклике',
                'Вы получили новый отклик на ваше объявление.',
                'projectnewspaper@yandex.ru',
                [post.user.email],
                fail_silently=False,
            )
            return redirect('ads:post_detail', pk=post.pk)

    comments = post.comments.all()
    form = CommentForm()
    category_url = reverse('ads:category_posts', args=[post.category])
    return render(request, 'ads/post_detail.html',
                  {'post': post, 'comments': comments, 'form': form, 'category_url': category_url})


@login_required
def user_comments(request):
    user = request.user
    comments = Comment.objects.filter(post__user=user)
    return render(request, 'ads/user_comments.html', {'comments': comments})


def accept_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if not comment.is_accepted:
        comment.is_accepted = True
        comment.is_private = False
        comment.save()

        # Отправка уведомления пользователю
        send_mail(
            'Ваш отклик был принят',
            'Ваш отклик на объявление был принят.',
            'projectnewspaper@yandex.ru',
            [comment.user.email],
            fail_silently=False,
        )
        messages.success(request, 'Отклик успешно принят.')

    # Перенаправление на страницу с откликами пользователя
    return redirect('ads:user_comments')


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.user == request.user:
        comment.delete()

    return redirect('ads:user_comments')


