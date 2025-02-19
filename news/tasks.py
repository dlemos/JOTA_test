from django.utils import timezone

from celery import shared_task

from .models import News


@shared_task
def check_and_publish_scheduled_news():
    News.objects.filter(
        status=News.Status.RASCUNHO,
        publising_date__lt=timezone.now()
    ).update(status=News.Status.PUBLICADO)
