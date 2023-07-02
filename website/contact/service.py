from django.core.mail import send_mail
from django.conf import settings


def send(user_email):
    send_mail(
        'Вы подписались на рассылку',  # тема письма
        'Мы будем присылать сообщения',  # текст письма
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )
