from celery import shared_task


@shared_task
def check_and_publish_scheduled_news():
    print("Hi!")
