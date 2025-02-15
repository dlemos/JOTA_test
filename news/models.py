from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import User


class Category(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(_("title"), max_length=1024)
    subtitle = models.CharField(_("subtitle"), max_length=1024)
    image = models.ImageField(_("image"))
    content = models.TextField(_("content"))
    publising_date = models.DateField(_("publishing_date"))
    author = models.ForeignKey(User, verbose_name=_("author"), on_delete=models.PROTECT)
    status = models.CharField(_("status"), choices={
        "R": "Rascunho",
        "P": "Publicado"
    }, default="R", max_length=1)
    # options here need to extended in the future
    category = models.ForeignKey(Category, verbose_name=_("category"), on_delete=models.PROTECT)
    is_pro_only = models.BooleanField(_("is_pro_only"), default=False)
