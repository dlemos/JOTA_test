import tempfile
import pathlib
from PIL import Image

import pytest

from django.core.files.base import File as DjangoFile

from rest_framework.test import APIClient
from rest_framework import status

from main.models import User
from news.models import Category, News


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.force_authenticate(admin_user)
    return client


@pytest.fixture
def unlogged_client(admin_user):
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
def news(author, category, image):
    return News.objects.create(**{
        "title": "Fixture News",
        "subtitle": "Just one more fixture",
        "image": DjangoFile(image, name=pathlib.Path(image.name).name),
        "content": "This is just a test to see what happens.",
        "publising_date": "2025-02-12",
        "status": "D",
        "is_pro_only": False,
        "author": author,
        "category": category
    })


def test_create_news(unlogged_client, author, category, image):
    response = unlogged_client.post('/news/', {
        "title": "This is just a test",
        "subtitle": "really",
        "image": image,
        "content": "This is just a test to see what happens.",
        "publising_date": "2025-02-12",
        "status": "D",
        "is_pro_only": False,
        "author": author.pk,
        "category": category.pk
    })
    assert response.status_code == status.HTTP_201_CREATED


def test_retrieve_news(unlogged_client, news):
    response = unlogged_client.get(f"/news/{news.pk}/")
    assert response.status_code == status.HTTP_200_OK


def test_update_news(unlogged_client, news):
    response = unlogged_client.get(f"/news/{news.pk}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] == "R"
    response = unlogged_client.patch(f"/news/{news.pk}/", {"status": "P"})
    assert response.status_code == status.HTTP_200_OK, response.data
    assert response.data["status"] == "P"


def test_delete_news(unlogged_client, news):
    assert News.objects.get(pk=news.pk)
    response = unlogged_client.delete(f"/news/{news.pk}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.data
    assert not News.objects.filter(pk=news.pk).exists()
