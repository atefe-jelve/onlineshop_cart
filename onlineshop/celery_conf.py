from celery import Celery
from celery.schedules import timedelta
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','onlineshop.settings')

celery_app = Celery('onlineshop')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

celery_app.conf.broker_url = 'amqp://'
celery_app.conf.result_backend = 'rpc://'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'json'
celery_app.conf.accept_content = ['json']
celery_app.conf.result_expires = timedelta(days=1)
celery_app.conf.task_always_eager = False
celery_app.conf.worker_prefetch_multiplier = 4
celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.timezone = 'Asia/Tehran'