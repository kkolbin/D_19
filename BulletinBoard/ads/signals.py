from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(user_signed_up)
def user_signed_up_handler(request, user, **kwargs):
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.username = request.POST['username']
    user.save()
