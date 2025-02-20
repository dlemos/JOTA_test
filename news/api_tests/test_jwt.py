import tempfile
import pathlib
from datetime import timedelta

from freezegun import freeze_time

from PIL import Image

import pytest

from django.core.files.base import File as DjangoFile
from django.contrib.auth.models import Group

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
def author():
    return User.objects.create(username="Nemo")


@pytest.fixture
def user_with_password():
    user = User.objects.create(username="Bob")
    user.set_password("tables")
    user.save()
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
        "status": "D",
        "is_pro_only": False,
        "author": author,
        "category": category
    })


@pytest.fixture(autouse=True)
def editor_group():
    group = Group.objects.create(name="Editor")
    yield group
    group.delete()


def test_existing_user_should_not_be_able_to_generate_a_token_with_wrong_password(unlogged_client, user_with_password):
    response = unlogged_client.post("/api/token/", {
        "username": user_with_password.username,
        "password": "not_the_correct_password"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.data


def test_existing_user_should_be_able_to_generate_a_token_with_correct_password(unlogged_client, user_with_password):
    response = unlogged_client.post("/api/token/", {"username": user_with_password.username, "password": "tables"})
    assert response.status_code == status.HTTP_200_OK, response.data
    assert "access" in response.data, "Access token not present on response"


def test_delete_should_fail_using_a_bad_JWT_token(unlogged_client, news):
    unlogged_client.credentials(HTTP_AUTHORIZATION="Bearer 123")
    response = unlogged_client.delete(f"/news/{news.pk}/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.data


def test_delete_news_using_valid_JWT_token(unlogged_client, admin_user, news):
    token = AccessToken.for_user(admin_user)
    unlogged_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = unlogged_client.delete(f"/news/{news.pk}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.data
    assert not News.objects.filter(pk=news.pk).exists()


def test_get_should_fail_with_expired_JWT_token(unlogged_client, admin_user, news):
    token = AccessToken.for_user(admin_user)
    token.set_exp(lifetime=-timedelta(days=1))
    unlogged_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = unlogged_client.get(f"/news/{news.pk}/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Should not be able to use an expired token"
    assert News.objects.filter(pk=news.pk).exists()


def test_get_should_be_possible_after_renew_expired_JWT_token(unlogged_client, user_with_password, news):
    response = unlogged_client.post("/api/token/", {"username": user_with_password.username, "password": "tables"})
    assert response.status_code == status.HTTP_200_OK, response.data
    assert "access" in response.data, "Access token not present on response"
    assert "refresh" in response.data, "Refresh token not present on response"

    refresh_token = response.data["refresh"]

    with freeze_time(timedelta(hours=1)):
        unlogged_client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data["access"]}")
        response = unlogged_client.delete(f"/news/{news.pk}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.content
        assert "Token is invalid or expired" in str(response.content)

        response = unlogged_client.post("/api/token/refresh/", {
            "refresh": refresh_token
        })
        assert response.status_code == status.HTTP_200_OK, response.content
        assert "access" in response.data, "Access token not present on response, after refresh"
