from unittest.mock import MagicMock

import mock
import pytest
from channels.auth import UserLazyObject
from channels.generic.websocket import WebsocketConsumer
from channels.testing import WebsocketCommunicator

from channels_ws_auth.middleware import WSAuthMiddleware, validate_key
from django.contrib.auth.models import AnonymousUser


@pytest.fixture
def populated_scope():
    scope = {}
    WSAuthMiddleware.populate_scope(mock.Mock(), scope)
    return scope


def test_populate_scope(populated_scope):
    assert "user" in populated_scope
    assert isinstance(populated_scope["user"], UserLazyObject)


@pytest.mark.django_db
def test_validate_key(ticket, user):
    ticket_user = validate_key(key=ticket.key)
    assert ticket_user == user


@pytest.mark.asyncio
async def test_resolve_scope_without_query_string(populated_scope):
    await WSAuthMiddleware.resolve_scope(mock.Mock(), populated_scope)

    assert "user" in populated_scope
    assert isinstance(populated_scope["user"]._wrapped, AnonymousUser)
    assert populated_scope["user"].is_anonymous


@pytest.mark.asyncio
async def test_resolve_scope_with_empty_query_string(populated_scope):
    populated_scope["query_string"] = b""

    await WSAuthMiddleware.resolve_scope(mock.Mock(), populated_scope)

    assert "user" in populated_scope
    assert isinstance(populated_scope["user"]._wrapped, AnonymousUser)
    assert populated_scope["user"].is_anonymous


@pytest.mark.asyncio
async def test_resolve_scope_query_string_key_empty(populated_scope):
    populated_scope["query_string"] = b"ticket="

    await WSAuthMiddleware.resolve_scope(mock.Mock(), populated_scope)

    assert "user" in populated_scope
    assert isinstance(populated_scope["user"]._wrapped, AnonymousUser)
    assert populated_scope["user"].is_anonymous


@pytest.mark.asyncio
async def test_resolve_scope_query_string_key_wrong(populated_scope):
    populated_scope["query_string"] = b"ticket=wrongkey"

    await WSAuthMiddleware.resolve_scope(mock.Mock(), populated_scope)

    assert "user" in populated_scope
    assert isinstance(populated_scope["user"]._wrapped, AnonymousUser)
    assert populated_scope["user"].is_anonymous


# @pytest.mark.asyncio
# async def test_resolve_scope_query_string_key_correct(user, ticket, populated_scope):
#     populated_scope["query_string"] = f"ticket={ticket.key}".encode()

#     ws_auth_middleware = mock.Mock(validate_key=WSAuthMiddleware.validate_key)
#     await WSAuthMiddleware.resolve_scope(ws_auth_middleware, populated_scope)

#     assert "user" in populated_scope
#     assert populated_scope["user"]._wrapped == user


# @pytest.mark.django_db
# @pytest.mark.asyncio
# async def test_ws_auth_middleware(user, ticket):
#     results = {}
#     class TestConsumer(WebsocketConsumer):
#         def connect(self):
#             results["connected"] = True
#             results["user"] = self.scope["user"]
#             self.accept()

#         def receive(self, text_data=None, bytes_data=None):
#             results["received"] = (text_data, bytes_data)
#             self.send(text_data=text_data, bytes_data=bytes_data)

#         def disconnect(self, code):
#             results["disconnected"] = code

#     communicator = WebsocketCommunicator(WSAuthMiddleware(TestConsumer), f"/?key={ticket.key}")
#     connected, _ = await communicator.connect()
#     assert connected
#     # await communicator(scope={"query_string": (ticket.key,)})
#     assert results['user'] == user
