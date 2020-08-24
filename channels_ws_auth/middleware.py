import logging
from urllib.parse import parse_qs

from channels.auth import UserLazyObject
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError

from .models import WSAuthTicket

LOGGER = logging.getLogger(__name__)


class WSAuthMiddleware(BaseMiddleware):
    """
    WebSocket validation middleware
    """

    def populate_scope(self, scope):
        """
        Insert a UserLazyObject in the scope to be
        later resolved with the proper user
        """
        if "user" not in scope:
            scope["user"] = UserLazyObject()

    def validate_key(self, key: str):
        """
        Return User if key is valid, else return AnonymousUser.
        """
        if key is None:
            return AnonymousUser()

        # if a key is given
        try:
            ticket = WSAuthTicket.objects.get(key=key)
        except (WSAuthTicket.DoesNotExist, ValidationError):
            LOGGER.info("Invalid ticket key %s", key)
        else:
            if not ticket.is_expired:
                user = ticket.user
                ticket.delete()
                return user
            LOGGER.info("Expired ticket %s", key)
            ticket.delete()

        return AnonymousUser()

    def get_key_from_scope(self, scope):
        """
        Return the key if it is in the query_string of the scope,
        otherwise return None
        """
        if "query_string" not in scope:
            return None

        query_string = parse_qs(scope["query_string"].decode())
        if "ticket" in query_string and len(query_string["ticket"]) == 1:
            return query_string["ticket"][0]
        return None

    async def resolve_scope(self, scope):
        key = self.get_key_from_scope(scope)
        scope["user"]._wrapped = await database_sync_to_async(self.validate_key)(key)
