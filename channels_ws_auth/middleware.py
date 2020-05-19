import logging
from urllib.parse import parse_qs

from asgiref.sync import sync_to_async
from channels.auth import UserLazyObject
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser

from .models import WSAuthTicket

LOGGER = logging.getLogger(__name__)


def validate_key(key):
    try:
        ticket = WSAuthTicket.objects.select_related("user").get(key=key)
    except WSAuthTicket.DoesNotExist:
        LOGGER.info("Invalid ticket %s", key)
    else:
        if not ticket.is_expired:
            user = ticket.user
        else:
            LOGGER.info("Expired ticket %s", key)
        ticket.delete()
    return user or AnonymousUser()


class WSAuthMiddleware(BaseMiddleware):
    """
    WebSocket validation middlewar
    """

    def populate_scope(self, scope):
        """
        Insert a UserLazyObject in the scope to be
        later resovled with the proper user
        """
        if "user" not in scope:
            scope["user"] = UserLazyObject()

    def validate_key(self, key):
        return validate_key(key)

    async def resolve_scope(self, scope):
        scope["user"]._wrapped = AnonymousUser()
        if "query_string" in scope:
            query_string = parse_qs(scope["query_string"].decode())
            if "ticket" in query_string and len(query_string["ticket"]) == 1:
                key = query_string["ticket"][0]
                scope["user"]._wrapped = await sync_to_async(self.validate_key)(key)
