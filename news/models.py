from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import User


class Category(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class News(models.Model):
    class Status(models.TextChoices):
        DRAFT = "D", _("draft")
        PUBLISHED = "P", _("published")

    title = models.CharField(_("title"), max_length=1024, help_text=_("The title of the news"))
    subtitle = models.CharField(_("subtitle"), max_length=1024, help_text=_("The text the goes right bellow the title"))
    image = models.ImageField(_("image"), help_text=_("A image that is intimatelly connected to the news"))
    content = models.TextField(_("content"), help_text=_("The body of the news"))
    publising_date = models.DateTimeField(_("publishing_date"), help_text=_("When this news should be published"))
    author = models.ForeignKey(
        User, verbose_name=_("author"), on_delete=models.PROTECT, help_text=_("The editor of this news")
    )
    status = models.CharField(
        _("status"), choices=Status, default=Status.DRAFT, max_length=1, help_text=_("Is this news pubblished or not?")
    )
    # options here need to extended in the future
    category = models.ForeignKey(
        Category, verbose_name=_("category"), on_delete=models.PROTECT, help_text=_("What vertical this news bellogs to")
    )
    is_pro_only = models.BooleanField(_("is_pro_only"), default=False, help_text=_("Is this news only for PRO readers?"))
