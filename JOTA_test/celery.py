import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "JOTA_test.settings")

app = Celery("JOTA_test")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
