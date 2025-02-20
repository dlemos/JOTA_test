import pytest

from rest_framework.test import APIClient
from rest_framework import status

from main.models import Subscription, User
from main.factories import UserFactory

from news.factories import CategoryFactory
from news.models import Category


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
    response = unlogged_client.get("/user/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_regular_user_should_not_be_able_to_access_the_user_endpoint(user_client):
    response = user_client.get("/user/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_admin_user_should_be_able_to_access_the_user_endpoint(admin_client):
    response = admin_client.get("/user/")
    assert response.status_code == status.HTTP_200_OK


def test_admin_user_should_be_able_to_create_new_user(admin_client):
    response = admin_client.post("/user/", {
        "username": "anewuser"
    })
    assert response.status_code == status.HTTP_201_CREATED, response.data


def test_admin_user_should_be_able_to_create_new_admin_user(admin_client):
    response = admin_client.post("/user/", {
        "username": "anewadminuser",
        "is_superuser": True
    })
    assert response.status_code == status.HTTP_201_CREATED, response.data
    assert User.objects.get(pk=response.data["id"]).is_superuser


def test_admin_user_should_be_able_to_create_new_user_with_a_subscription(admin_client):
    category = CategoryFactory()
    response = admin_client.post("/user/", {
        "username": "anewuser",
        "subscription": {
            "verticals": [category.pk],
            "plan": Subscription.Plans.JOTA_PRO
        }
    }, format="json")
    assert response.status_code == status.HTTP_201_CREATED, response.data
    response = admin_client.get(f"/user/{response.data["id"]}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data['subscription']


def test_admin_user_should_be_able_to_destroy_user(admin_client):
    user = UserFactory(username="tobedeleted")
    assert User.objects.filter(id=user.pk).exists()
    response = admin_client.delete(f"/user/{user.pk}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.content
    assert not User.objects.filter(id=user.pk).exists()


def test_admin_user_should_be_able_to_update_user(admin_client):
    user = UserFactory(username="tobechanged")
    assert User.objects.filter(id=user.pk).exists()
    assert not User.objects.filter(id=user.pk, username="nowchanged").exists()
    response = admin_client.patch(f"/user/{user.pk}/", {"username": "nowchanged"})
    assert response.status_code == status.HTTP_200_OK, response.content
    assert User.objects.filter(id=user.pk, username="nowchanged").exists()
