import tempfile
from PIL import Image

import pytest

from rest_framework.test import APIClient
from rest_framework import status

@pytest.fixture
def unlogged_client(admin_user):
    client = APIClient()
    return client

def test_unlogged_user_should_be_able_to_access_the_api(unlogged_client):
    unlogged_client.get('/')

def test_admin_user_should_be_able_to_access_the_api(admin_client):
    admin_client.get('/')