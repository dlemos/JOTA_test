from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Subscription(models.Model):

    class Plans(models.TextChoices):
        JOTA_INFO = "I", "JOTA_Info"
        JOTA_PRO = "P"

    user = models.OneToOneField(User, on_delete=models.PROTECT, help_text=_("User associated with this subscription"))
    verticals = models.ManyToManyField(
        "news.Category", help_text=_("Categories of PRO news this subscriber have access to")
    )
    plan = models.CharField(_("plan"), max_length=1, choices=Plans, help_text=_("User's plan"))
