import logging
from contextlib import suppress

from django.contrib.auth import get_user_model
from django.db import IntegrityError

LOGGER = logging.getLogger(__name__)


def auto_create_user(*args, **kwargs):
    LOGGER.warning(
        "Attention: attempting to create *REALLY* unsafe User, do not run this on production!"
    )
    user_model = get_user_model()
    with suppress(IntegrityError):
        user_model.objects.create_user(username="user", password="password")
