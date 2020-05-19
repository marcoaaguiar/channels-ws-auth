import logging
from datetime import timedelta
from functools import wraps

from django.conf import settings
from django.utils import timezone

from channels_ws_auth.models import WSAuthTicket

LOGGER = logging.getLogger(__name__)


def remove_expired_tickets():
    expired_tickets = WSAuthTicket.objects.filter(
        created__lte=timezone.now() - timedelta(seconds=settings.WS_AUTH_DURATION)
    )

    n_tickets_deleted = expired_tickets.delete()
    LOGGER.info("Removed %s expired tokens", n_tickets_deleted)


def is_authenticated(cls):
    _connect = cls.connect

    @wraps(cls.connect)
    def connect(self):
        if not "user" in self.scope or self.scope["user"].is_anonymous:
            LOGGER.info("User not logged in, closing connection")
            self.close()
            return
        _connect(self)

    setattr(cls, "connect", connect)
    return cls
