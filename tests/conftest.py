import pytest
from rest_framework.test import APIClient


@pytest.fixture
@pytest.mark.django_db
def user(django_user_model):
    return django_user_model.objects.create_user(username="user")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, user, api_client):
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
