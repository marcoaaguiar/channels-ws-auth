import logging
from urllib.parse import parse_qs

from channels.auth import UserLazyObject
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser

from .models import WSAuthTicket

LOGGER = logging.getLogger(__name__)


@database_sync_to_async
def validate_key(key, tenant):
    user = None
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
    return user


class WSTicketAuthMiddleware(BaseMiddleware):
    def populate_scope(self, scope):
        if "user" not in scope:
            scope["user"] = UserLazyObject()

    async def resolve_scope(self, scope):
        scope["user"]._wrapped = AnonymousUser()  # pylint: disable=protected-access

        if "query_string" in scope:
            query_string = parse_qs(scope["query_string"].decode())
            if "ticket" in query_string and len(query_string["ticket"]) == 1:
                key = query_string["ticket"][0]
                user = await validate_key(key, scope["tenant"])
                if user:
                    scope["user"]._wrapped = user  # pylint: disable=protected-access
