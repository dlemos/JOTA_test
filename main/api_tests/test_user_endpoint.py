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
def user_client():
    user = User.objects.create()
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.fixture
def category():
    return Category.objects.create(name="Tecnologia")


def test_unlogged_user_should_not_be_able_to_access_the_user_endpoint(unlogged_client):
    response = unlogged_client.get(f"/user/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_regular_user_should_not_be_able_to_access_the_user_endpoint(user_client):
    response = user_client.get(f"/user/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_admin_user_should_be_able_to_access_the_user_endpoint(admin_client):
    response = admin_client.get(f"/user/")
    assert response.status_code == status.HTTP_200_OK
