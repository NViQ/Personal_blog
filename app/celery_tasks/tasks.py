from celery import shared_task
from django.contrib.auth.models import User
from newsfeed.utils import send_daily_email as console_send_daily_email


@shared_task
def send_daily_newsfeed_to_console():
    for user in User.objects.all():
        console_send_daily_email(user.id)



@shared_task
def say_hello():
    print('Hello, world!')
