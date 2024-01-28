from django.urls import path
from . import views
from allauth.account.views import LoginView, LogoutView, SignupView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from .views import (PostCreateView,
                    PostDetailView,
                    PostEditView,
                    HomeView,
                    profile_view,
                    AuthorProfileView,
                    CategoryPostsView,
                    posts,
                    user_comments,
                    accept_comment,
                    create_comment,
                    delete_comment)


app_name = 'ads'

urlpatterns = [
    path('login/', LoginView.as_view(), name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
    path('signup/', SignupView.as_view(), name='account_signup'),
    path('profile/<str:username>/', profile_view, name='profile_view'),
    path('password/change/', PasswordChangeView.as_view(), name='account_change_password'),

    path('', HomeView.as_view(), name='home'),
    path('create_post/', PostCreateView.as_view(), name='create_post'),
    path('post_detail/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('edit_post/<int:pk>/', PostEditView.as_view(), name='edit_post'),
    path('author_profile/<str:username>/', AuthorProfileView.as_view(), name='author_profile'),
    path('category_posts/<str:category>/', CategoryPostsView.as_view(), name='category_posts'),
    path('user_comments/', user_comments, name='user_comments'),
    path('accept_comment/<int:comment_id>/', accept_comment, name='accept_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('create_comment/<int:pk>/', create_comment, name='create_comment'),
]

