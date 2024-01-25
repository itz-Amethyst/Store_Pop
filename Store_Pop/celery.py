import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Store_Pop.settings")

# Should be imported in __init__ file either
celery = Celery('Store_Pop')
celery.config_from_object('django.conf:settings', namespace = 'CELERY')
celery.autodiscover_tasks()