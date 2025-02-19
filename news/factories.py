import factory

from main.factories import UserFactory

from .models import Category, News


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category


class NewsFactory(factory.django.DjangoModelFactory):
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = News
