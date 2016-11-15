from  __future__ import absolute_import
from celery import task
from celery import shared_task
from rango.models import celeryResponse

@shared_task
def add(x,y):
    return x + y

@shared_task
def hello_message(message):
    # writes a message to the database
    logged_message = celeryResponse(message = message)
    logged_message.save()
    # saving to database
