from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import DailyNewsletter
from ads.models import Post


@shared_task
def send_daily_newsletter():
    # Определение временного интервала за предыдущий день
    yesterday = timezone.now() - timezone.timedelta(days=1)

    # Получение всех объявлений, добавленных за предыдущий день
    new_posts = Post.objects.filter(created_at__gte=yesterday)

    # Отправление рассылки каждому пользователю
    for user in User.objects.all():
        # Проверка, была ли уже отправлена рассылка для данного пользователя сегодня
        if not DailyNewsletter.objects.filter(user=user, date_sent=yesterday).exists():
            # Создание записи о рассылке
            newsletter = DailyNewsletter.objects.create(user=user, date_sent=yesterday)

            # Добавление всех новых объявлений к рассылке
            newsletter.posts.set(new_posts)
            newsletter.save()

            # Отправка письма с сылками на объявления
            subject = 'Ежедневная рассылка объявлений'
            message = f'Привет, {user.username}! Вот все новые объявления с прошлого дня:\n\n'
            for post in new_posts:
                message += f'{post.title} - {post.get_absolute_url()}\n'
            send_mail(subject, message, 'projectnewspaper@yandex.ru', [user.email])


