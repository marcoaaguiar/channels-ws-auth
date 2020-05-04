import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

import channels_ws_auth.settings as app_settings


class WSAuthTicket(models.Model):
    class Meta:
        verbose_name = _("WS Auth Ticket")
        verbose_name_plural = _("WS Auth Tickets")

    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    def __str__(self):
        return self.key

    @property
    def is_expired(self):
        time_elapsed = timezone.now() - self.created
        return time_elapsed > timedelta(
            seconds=getattr(
                settings,
                "CHANNELS_WS_AUTH_EXPIRATION",
                app_settings.CHANNELS_WS_AUTH_EXPIRATION,
            )
        )
