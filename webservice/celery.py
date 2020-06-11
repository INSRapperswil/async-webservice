from celery import Celery
from os import environ


environ.setdefault('DJANGO_SETTINGS_MODULE', 'webservice.settings')

celery_app = Celery('webservice')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
