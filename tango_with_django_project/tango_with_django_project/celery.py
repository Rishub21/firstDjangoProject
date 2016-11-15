
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
#django.setup()
app = Celery('tango_with_django_project')

app.config_from_object('django.conf:settings') # project settings
#app.config.update( CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',)
#app.conf.update(CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend',)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) # looks for a tasks.py file in every single app, to see what celery needs to do


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
