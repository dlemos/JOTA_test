# flake8: noqa
import pytest
import factory

from django.contrib.auth.models import Group

from rest_framework import status
from rest_framework.test import APIClient

from rest_framework_simplejwt.tokens import AccessToken

from main.factories import EditorFactory, UserFactory, ProUserFactory

from news.models import News
from news.factories import CategoryFactory, NewsFactory


pytestmark = pytest.mark.django_db


@pytest.fixture
def unlogged_client():
    client = APIClient()
    return client


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    token = AccessToken.for_user(admin_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture(autouse=True)
def editor_group():
    return Group.objects.create(name="Editor")


@pytest.fixture
def editor_user(editor_group):
    editor = EditorFactory()
    # FIXME: This should not be neccessery, it should be done by the factory
    # but it's not working. Check the factory for the error message.
    editor.groups.set([editor_group])
    return editor


@pytest.fixture
def categories():
    return CategoryFactory.create_batch(2, name=factory.Sequence(lambda n: 'Category {0}'.format(n)))


@pytest.mark.parametrize(
            "publising_date, is_pro_only, status,              expected_http_status", [
    pytest.param("2024-01-10",  False,  News.Status.DRAFT,   status.HTTP_404_NOT_FOUND,  id="can_not_read_unpublished_jota_info_news"),
    pytest.param("2024-01-10",  False,  News.Status.PUBLISHED,  status.HTTP_200_OK,         id="can_read_published_jota_info_news"),
    pytest.param("2024-01-10",  True,   News.Status.PUBLISHED,  status.HTTP_404_NOT_FOUND,  id="can_not_read_jota_pro_news"),
    pytest.param("2024-01-10",  True,   News.Status.DRAFT,   status.HTTP_404_NOT_FOUND,  id="can_not_read_unpublished_pro_news"),
    ])
def test_unlogged_reader(unlogged_client, publising_date, is_pro_only, status, expected_http_status):
    news = NewsFactory(
        publising_date=publising_date,
        is_pro_only=is_pro_only,
        status=status
    )
    response = unlogged_client.get(f"/news/{news.pk}/")
    assert response.status_code == expected_http_status, response.content

    
@pytest.mark.parametrize(
            "publising_date, is_pro_only, status,              expected_http_status", [
    pytest.param("2024-01-10",  False,  News.Status.DRAFT,   status.HTTP_401_UNAUTHORIZED,  id="unpublished_jota_info_news"),
    pytest.param("2024-01-10",  False,  News.Status.PUBLISHED,  status.HTTP_401_UNAUTHORIZED,  id="published_jota_info_news"),
    pytest.param("2024-01-10",  True,   News.Status.PUBLISHED,  status.HTTP_401_UNAUTHORIZED,  id="jota_pro_news"),
    pytest.param("2024-01-10",  True,   News.Status.DRAFT,   status.HTTP_401_UNAUTHORIZED,  id="unpublished_pro_news"),
    ])
def test_unlogged_reader_can_not_patch(unlogged_client, publising_date, is_pro_only, status, expected_http_status):
    news = NewsFactory(
        title="Original title",
        publising_date=publising_date,
        is_pro_only=is_pro_only,
        status=status
    )
    response = unlogged_client.patch(f"/news/{news.pk}/", {"title": "New Title"})
    assert response.status_code == expected_http_status, response.content


@pytest.mark.parametrize(
            "publising_date, is_pro_only, status,              expected_http_status", [
    pytest.param("2024-01-10",  False,  News.Status.DRAFT,   status.HTTP_200_OK,  id="unpublished_jota_info_news"),
    pytest.param("2024-01-10",  False,  News.Status.PUBLISHED,  status.HTTP_200_OK,  id="published_jota_info_news"),
    pytest.param("2024-01-10",  True,   News.Status.PUBLISHED,  status.HTTP_200_OK,  id="jota_pro_news"),
    pytest.param("2024-01-10",  True,   News.Status.DRAFT,   status.HTTP_200_OK,  id="unpublished_pro_news"),
    ])
def test_admin_can_read(admin_client, publising_date, is_pro_only, status, expected_http_status):
    news = NewsFactory(
        publising_date=publising_date,
        is_pro_only=is_pro_only,
        status=status
    )
    response = admin_client.get(f"/news/{news.pk}/")
    assert response.status_code == expected_http_status, response.content


@pytest.mark.parametrize(
            "publising_date, is_pro_only, status,              expected_http_status", [
    pytest.param("2024-01-10",  False,  News.Status.DRAFT,   status.HTTP_204_NO_CONTENT,  id="unpublished_jota_info_news"),
    pytest.param("2024-01-10",  False,  News.Status.PUBLISHED,  status.HTTP_204_NO_CONTENT,  id="published_jota_info_news"),
    pytest.param("2024-01-10",  True,   News.Status.PUBLISHED,  status.HTTP_204_NO_CONTENT,  id="jota_pro_news"),
    pytest.param("2024-01-10",  True,   News.Status.DRAFT,   status.HTTP_204_NO_CONTENT,  id="unpublished_pro_news"),
    ])
def test_admin_can_delete(admin_client, publising_date, is_pro_only, status, expected_http_status):
    news = NewsFactory(
        publising_date=publising_date,
        is_pro_only=is_pro_only,
        status=status
    )
    response = admin_client.delete(f"/news/{news.pk}/")
    assert response.status_code == expected_http_status, response.content

@pytest.mark.parametrize(
            "publising_date, is_pro_only, status,              expected_http_status", [
    pytest.param("2024-01-10",  False,  News.Status.DRAFT,   status.HTTP_200_OK,  id="unpublished_jota_info_news"),
    pytest.param("2024-01-10",  False,  News.Status.PUBLISHED,  status.HTTP_200_OK,  id="published_jota_info_news"),
    pytest.param("2024-01-10",  True,   News.Status.PUBLISHED,  status.HTTP_200_OK,  id="jota_pro_news"),
    pytest.param("2024-01-10",  True,   News.Status.DRAFT,   status.HTTP_200_OK,  id="unpublished_pro_news"),
    ])
def test_admin_can_patch(admin_client, publising_date, is_pro_only, status, expected_http_status):
    news = NewsFactory(
        title="Original title",
        publising_date=publising_date,
        is_pro_only=is_pro_only,
        status=status
    )
    response = admin_client.patch(f"/news/{news.pk}/", {"title": "New Title"})
    assert response.status_code == expected_http_status, response.content
    news.refresh_from_db()
    assert news.title == "New Title"


@pytest.mark.parametrize(
            "publising_date, is_pro_only, status,              expected_http_status", [
    pytest.param("2024-01-10",  False,  News.Status.DRAFT,   status.HTTP_200_OK,  id="unpublished_jota_info_news"),
    pytest.param("2024-01-10",  False,  News.Status.PUBLISHED,  status.HTTP_200_OK,  id="published_jota_info_news"),
    pytest.param("2024-01-10",  True,   News.Status.PUBLISHED,  status.HTTP_200_OK,  id="jota_pro_news"),
    pytest.param("2024-01-10",  True,   News.Status.DRAFT,   status.HTTP_200_OK,  id="unpublished_pro_news"),
    ])
def test_editor_can_read_their_own(unlogged_client, editor_user, publising_date, is_pro_only, status, expected_http_status):
    token = AccessToken.for_user(editor_user)
    unlogged_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    news = NewsFactory(
        publising_date=publising_date,
        is_pro_only=is_pro_only,
        status=status,
        author=editor_user
    )
    response = unlogged_client.get(f"/news/{news.pk}/")
    assert response.status_code == expected_http_status, response.content


@pytest.mark.parametrize(
            "publising_date, is_pro_only, status,              expected_http_status", [
    pytest.param("2024-01-10",  False,  News.Status.DRAFT,   status.HTTP_404_NOT_FOUND,  id="unpublished_jota_info_news"),
    pytest.param("2024-01-10",  False,  News.Status.PUBLISHED,  status.HTTP_404_NOT_FOUND,  id="published_jota_info_news"),
    pytest.param("2024-01-10",  True,   News.Status.PUBLISHED,  status.HTTP_404_NOT_FOUND,  id="jota_pro_news"),
    pytest.param("2024-01-10",  True,   News.Status.DRAFT,   status.HTTP_404_NOT_FOUND,  id="unpublished_pro_news"),
    ])
def test_editor_can_not_read_other_editor(unlogged_client, editor_user, publising_date, is_pro_only, status, expected_http_status):
    token = AccessToken.for_user(editor_user)
    unlogged_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    news = NewsFactory(
        publising_date=publising_date,
        is_pro_only=is_pro_only,
        status=status,
        author=UserFactory(username="other_user")
    )
    response = unlogged_client.get(f"/news/{news.pk}/")
    assert response.status_code == expected_http_status, response.content


@pytest.mark.parametrize(
            "publising_date, is_pro_only, status,              expected_http_status", [
    pytest.param("2024-01-10",  False,  News.Status.DRAFT,   status.HTTP_404_NOT_FOUND,  id="unpublished_jota_info_news"),
    pytest.param("2024-01-10",  False,  News.Status.PUBLISHED,  status.HTTP_404_NOT_FOUND,  id="published_jota_info_news"),
    pytest.param("2024-01-10",  True,   News.Status.PUBLISHED,  status.HTTP_404_NOT_FOUND,  id="jota_pro_news"),
    pytest.param("2024-01-10",  True,   News.Status.DRAFT,   status.HTTP_404_NOT_FOUND,  id="unpublished_pro_news"),
    ])
def test_editor_can_not_patch_other_editor(unlogged_client, editor_user, publising_date, is_pro_only, status, expected_http_status):
    token = AccessToken.for_user(editor_user)
    unlogged_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    news = NewsFactory(
        title="Original Title",
        publising_date=publising_date,
        is_pro_only=is_pro_only,
        status=status,
        author=UserFactory(username="user_b")
    )
    response = unlogged_client.patch(f"/news/{news.pk}/", {"title": "New Title"})
    assert response.status_code == expected_http_status, response.content


@pytest.mark.parametrize(
            "publising_date, is_pro_only, status,              expected_http_status", [
    pytest.param("2024-01-10",  False,  News.Status.DRAFT,   status.HTTP_201_CREATED,  id="unpublished_jota_info_news"),
    pytest.param("2024-01-10",  False,  News.Status.PUBLISHED,  status.HTTP_201_CREATED,  id="published_jota_info_news"),
    pytest.param("2024-01-10",  True,   News.Status.PUBLISHED,  status.HTTP_201_CREATED,  id="jota_pro_news"),
    pytest.param("2024-01-10",  True,   News.Status.DRAFT,   status.HTTP_201_CREATED,  id="unpublished_pro_news"),
    ])
def test_editor_can_create(unlogged_client, editor_user, categories, publising_date, is_pro_only, status, expected_http_status):
    token = AccessToken.for_user(editor_user)
    unlogged_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = unlogged_client.post(f"/news/", {
        "title": "Some title",
        "publising_date": publising_date,
        "is_pro_only": is_pro_only,
        "status": status,
        "author": editor_user.pk,
        "category": categories[0].pk,
        "subtitle": "A short subtitle",
        "image": b'',
        "content": "Contente"
    })
    assert response.status_code == expected_http_status, response.content


@pytest.mark.parametrize(
            "publising_date, is_pro_only, status,              expected_http_status", [
    pytest.param("2024-01-10",  False,  News.Status.DRAFT,   status.HTTP_404_NOT_FOUND,  id="not_read_unpublished_jota_info_news"),
    pytest.param("2024-01-10",  False,  News.Status.PUBLISHED,  status.HTTP_200_OK,         id="read_published_jota_info_news"),
    pytest.param("2024-01-10",  True,   News.Status.PUBLISHED,  status.HTTP_404_NOT_FOUND,  id="not_read_jota_pro_news"),
    pytest.param("2024-01-10",  True,   News.Status.DRAFT,   status.HTTP_404_NOT_FOUND,  id="not_read_unpublished_pro_news"),
    ])
def test_for_news_not_in_his_verticals_pro_reader_can(unlogged_client, categories, publising_date, is_pro_only, status, expected_http_status):
    pro_reader = ProUserFactory(username="proreader", subscription__verticals=(categories[1],))
    token = AccessToken.for_user(pro_reader)
    unlogged_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    news = NewsFactory(
        publising_date=publising_date,
        is_pro_only=is_pro_only,
        status=status,
        category=categories[0]
    )
    response = unlogged_client.get(f"/news/{news.pk}/")
    assert response.status_code == expected_http_status, response.content


@pytest.mark.parametrize(
            "publising_date, is_pro_only, status,              expected_http_status", [
    pytest.param("2024-01-10",  False,  News.Status.DRAFT,   status.HTTP_404_NOT_FOUND,  id="not_read_unpublished_jota_info_news"),
    pytest.param("2024-01-10",  False,  News.Status.PUBLISHED,  status.HTTP_200_OK,         id="read_published_jota_info_news"),
    pytest.param("2024-01-10",  True,   News.Status.PUBLISHED,  status.HTTP_200_OK,  id="can_read_jota_pro_news"),
    pytest.param("2024-01-10",  True,   News.Status.DRAFT,   status.HTTP_404_NOT_FOUND,  id="can_not_read_unpublished_pro_news"),
    ])
def test_for_news_in_his_verticals_pro_reader_can(unlogged_client, categories, publising_date, is_pro_only, status, expected_http_status):
    pro_reader = ProUserFactory.create(username="proreader", subscription__verticals=(categories[1],))
    token = AccessToken.for_user(pro_reader)
    unlogged_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    news = NewsFactory(
        publising_date=publising_date,
        is_pro_only=is_pro_only,
        status=status,
        category=categories[1]
    )
    response = unlogged_client.get(f"/news/{news.pk}/")
    assert response.status_code == expected_http_status, response.content
