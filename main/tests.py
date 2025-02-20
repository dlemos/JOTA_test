import pytest

from .models import Subscription
from news.models import Category


@pytest.fixture
def categories():
    return Category.objects.bulk_create([
        Category(name="Cat 1"),
        Category(name="Cat 2")
    ])


def test_create_custom_user_model(django_user_model):
    django_user_model.objects.create_user(username="bob")


def test_user_can_have_a_subscription(django_user_model, categories):
    sub = Subscription.objects.create(plan='I')
    sub.verticals.set(categories)
    user = django_user_model.objects.create_user(subscription=sub, username="new_user")
    assert user.subscription
    assert user.subscription.plan == 'I'
    assert all(user.subscription.verticals.contains(category) for category in categories)
