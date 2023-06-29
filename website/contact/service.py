from django.core.mail import send_mail


def send(user_email):
    send_mail(
        'Вы подписались на рассылку', # тема письма
        'Мы будем присылать сообщения', # текст письма
        'opt774@yandex.ru',
        [user_email],
        fail_silently=False
    )
