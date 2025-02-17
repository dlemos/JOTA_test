from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    verticals = models.ManyToManyField("news.Category")
    plan = models.CharField(max_length=1, choices={"I": "JOTA Info", "P": "JOTA PRO"})
