from celery_app import app
from .service import send
# from .models import Contact
# from django.core.mail import send_mail

@app.task
def send_spam_email(user_email):
    send(user_email)
    print('Письмо отправленно')



# @app.task
# def send_beat_email():
#     for contact in Contact.objects.all():
#         send_mail(
#             'Вы подписались на рассылку',  # тема письма
#             'Мы будем присылать сообщения',  # текст письма
#             'opt774@yandex.ru',
#             [contact.email],
#             fail_silently=False
#         )
