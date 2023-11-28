import time

from celery import shared_task
from user.utils import send_email

@shared_task(serializer='json', name="send_mail")
def send_email_fun(request):
    time.sleep(20)
    send_email(request, request.user)
