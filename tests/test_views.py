"""
test_channels-ws-auth
------------

Tests for `channels-ws-auth` models module.
"""
import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from channels_ws_auth.models import WSAuthTicket


def test_require_authentication(client):
    response = client.post("/")
    assert response.status_code == 403


def test_request(api_client_with_credentials):
    response = api_client_with_credentials.post("/")
    assert response.status_code == 201


def test_request_creates(api_client_with_credentials):
    response = api_client_with_credentials.post("/")
    assert WSAuthTicket.objects.count() == 1


def test_request_creates_with_user(user, api_client_with_credentials):
    response = api_client_with_credentials.post("/")
    ticket = WSAuthTicket.objects.last()
    assert ticket.user == user


def test_request_body_content(user, api_client_with_credentials):
    response = api_client_with_credentials.post("/")
    ticket = WSAuthTicket.objects.last()
    body = response.json()
    assert "key" in body
    assert body["key"] == str(ticket.key)
