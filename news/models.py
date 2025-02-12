from main.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=80)

class News(models.Model):
    title = models.CharField(max_length=1024)
    subtitle = models.CharField(max_length=1024)
    image = models.ImageField()
    content = models.TextField()
    pubblising_date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(choices={
        "R": "Rascunho",
        "P": "Publicado"
    }, default="R", max_length=1)
    # options here need to extended in the future
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    is_pro_only = models.BooleanField(default=False)