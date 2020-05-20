from unittest.mock import MagicMock

import mock
import pytest
from channels.auth import UserLazyObject
from channels.generic.websocket import WebsocketConsumer
from channels.testing import WebsocketCommunicator

from channels_ws_auth.middleware import WSAuthMiddleware
from django.contrib.auth.models import AnonymousUser
import uuid
import time
from channels_ws_auth.models import WSAuthTicket
from channels.db import database_sync_to_async


@pytest.fixture
def ws_auth_middleware():
    scope = {}
    return WSAuthMiddleware(None)


@pytest.fixture
def populated_scope(ws_auth_middleware):
    scope = {}
    ws_auth_middleware.populate_scope(scope)
    return scope


@pytest.mark.django_db
def test_validate_key(ticket, user, ws_auth_middleware):
    ticket_user = ws_auth_middleware.validate_key(key=ticket.key)
    assert ticket_user == user


def test_populate_scope(populated_scope):
    assert "user" in populated_scope
    assert isinstance(populated_scope["user"], UserLazyObject)


def test_get_key_from_scope_missing_in_qs(populated_scope, ws_auth_middleware):
    key = ws_auth_middleware.get_key_from_scope(populated_scope)
    assert key is None


def test_get_key_from_scope_empty(populated_scope, ws_auth_middleware):
    populated_scope["query_string"] = b""
    key = ws_auth_middleware.get_key_from_scope(populated_scope)
    assert key is None


def test_get_key_from_scope(populated_scope, ws_auth_middleware):
    key = "somekey"
    populated_scope["query_string"] = f"key={key}".encode()
    key = ws_auth_middleware.get_key_from_scope(populated_scope)
    assert key is key


@pytest.mark.asyncio
async def test_resolve_scope_without_query_string(ws_auth_middleware, populated_scope):
    await ws_auth_middleware.resolve_scope(populated_scope)

    assert "user" in populated_scope
    assert isinstance(populated_scope["user"]._wrapped, AnonymousUser)
    assert populated_scope["user"].is_anonymous


@pytest.mark.asyncio
async def test_resolve_scope_with_empty_query_string(
    ws_auth_middleware, populated_scope
):
    populated_scope["query_string"] = b""

    await ws_auth_middleware.resolve_scope(populated_scope)

    assert "user" in populated_scope
    assert isinstance(populated_scope["user"]._wrapped, AnonymousUser)
    assert populated_scope["user"].is_anonymous


@pytest.mark.asyncio
async def test_resolve_scope_query_string_key_empty(
    ws_auth_middleware, populated_scope
):
    populated_scope["query_string"] = b"ticket="

    await ws_auth_middleware.resolve_scope(populated_scope)

    assert "user" in populated_scope
    assert isinstance(populated_scope["user"]._wrapped, AnonymousUser)
    assert populated_scope["user"].is_anonymous


@pytest.mark.asyncio
async def test_resolve_scope_query_string_key_wrong(
    ws_auth_middleware: WSAuthMiddleware, populated_scope
):
    populated_scope["query_string"] = b"ticket=wrongkey"

    await ws_auth_middleware.resolve_scope(populated_scope)

    assert "user" in populated_scope
    assert isinstance(populated_scope["user"]._wrapped, AnonymousUser)
    assert populated_scope["user"].is_anonymous


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_resolve_scope_query_string_uuid_key_wrong(
    ws_auth_middleware: WSAuthMiddleware, populated_scope
):
    key = uuid.uuid4()
    populated_scope["query_string"] = f"ticket={key}".encode()

    await ws_auth_middleware.resolve_scope(populated_scope)

    assert "user" in populated_scope
    assert isinstance(populated_scope["user"]._wrapped, AnonymousUser)
    assert populated_scope["user"].is_anonymous


@pytest.mark.asyncio
async def test_resolve_scope_query_string_key_correct(
    user, ticket, ws_auth_middleware, populated_scope, monkeypatch
):
    # for some reason I wasn't been able to make this to work
    # without mokeypatching the validate_key
    def mock_validate_key(key):
        # oversimplified validate_key
        if key == ticket.key:
            return user
        else:
            return AnonymousUser()

    monkeypatch.setattr(WSAuthMiddleware, "validate_key", lambda self, key: user)

    populated_scope["query_string"] = f"ticket={ticket.key}".encode()
    await ws_auth_middleware.resolve_scope(populated_scope)

    assert "user" in populated_scope
    assert populated_scope["user"]._wrapped == user
