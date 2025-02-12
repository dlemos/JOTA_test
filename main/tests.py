import pytest

def test_create_custom_user_model(django_user_model):
    django_user_model.objects.create_user(username="bob")