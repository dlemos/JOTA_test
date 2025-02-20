import pytest
import pathlib
import tempfile

from PIL import Image

from freezegun import freeze_time

from django.core.files.base import File as DjangoFile

from rest_framework.test import APIClient

from main.models import User

from .tasks import check_and_publish_scheduled_news
from .models import News, Category
from .factories import NewsFactory


pytestmark = pytest.mark.django_db


@pytest.fixture
def unlogged_client():
    client = APIClient()
    return client


@pytest.fixture
def author():
    return User.objects.create(username="Nemo")


@pytest.fixture
def category():
    return Category.objects.create(name="Tecnologia")


@pytest.fixture
def image():
    img = Image.new("RGB", (2, 2))
    tmp_file = tempfile.NamedTemporaryFile(suffix=".png", delete_on_close=True)
    img.save(tmp_file)
    tmp_file.seek(0)
    return tmp_file


@pytest.fixture
def unpublished_news(author, category, image):
    return News.objects.create(**{
        "title": "Fixture News",
        "subtitle": "Just one more fixture",
        "image": DjangoFile(image, name=pathlib.Path(image.name).name),
        "content": "This is just a test to see what happens.",
        "publising_date": "2025-02-12",
        "status": News.Status.DRAFT,
        "is_pro_only": False,
        "author": author,
        "category": category
    })


def test_unlogged_user_should_be_able_to_access_the_api(unlogged_client):
    unlogged_client.get('/')


def test_admin_user_should_be_able_to_access_the_api(admin_client):
    admin_client.get('/')


@freeze_time("2024-01-01 10:00 +00:00")
def test_check_and_publish_scheduled_news(unpublished_news):
    news = NewsFactory(publising_date="2024-01-01 09:59 +00:00", status=News.Status.DRAFT)
    check_and_publish_scheduled_news()
    assert not News.objects.filter(pk=news.pk, status=News.Status.DRAFT).exists()
    assert News.objects.filter(pk=news.pk, status=News.Status.PUBLISHED).exists()
