import tempfile
import pathlib
from PIL import Image

import pytest

from django.contrib.auth.models import Group
from django.core.files.base import File as DjangoFile

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from main.models import User
from news.models import Category, News


pytestmark = pytest.mark.django_db


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
def author(editor_group):
    user = User.objects.create(username="Nemo")
    user.groups.add(editor_group)
    return user


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
        "status": "P",
        "is_pro_only": False,
        "author": author,
        "category": category
    })


@pytest.fixture(autouse=True)
def editor_group():
    group = Group.objects.create(name="Editor")
    yield group
    group.delete()


def test_create_news(unlogged_client, author, category, image):
    token = AccessToken.for_user(author)
    unlogged_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
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
    assert response.status_code == status.HTTP_201_CREATED, response.data


def test_retrieve_news(unlogged_client, news):
    response = unlogged_client.get(f"/news/{news.pk}/")
    assert response.status_code == status.HTTP_200_OK


def test_update_test_update_newsnews(unlogged_client, author, news):
    token = AccessToken.for_user(author)
    unlogged_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = unlogged_client.get(f"/news/{news.pk}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["subtitle"] == "Just one more fixture"
    new_response = unlogged_client.patch(f"/news/{news.pk}/", {"subtitle": "This is a subtitle"})
    assert new_response.status_code == status.HTTP_200_OK, response.data
    assert new_response.data["subtitle"] == "This is a subtitle"


def test_delete_news(unlogged_client, author, news):
    assert News.objects.get(pk=news.pk)
    token = AccessToken.for_user(author)
    unlogged_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = unlogged_client.delete(f"/news/{news.pk}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.data
    assert not News.objects.filter(pk=news.pk).exists()
