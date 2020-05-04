#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_channels-ws-auth
------------

Tests for `channels-ws-auth` models module.
"""

from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

import channels_ws_auth.settings as app_settings
from channels_ws_auth.models import WSAuthTicket


@pytest.fixture
@pytest.mark.django_db
def ticket(user):
    return WSAuthTicket.objects.create(user=user)


@pytest.mark.django_db
def test_require_user():
    with pytest.raises(IntegrityError):
        WSAuthTicket.objects.create()


@pytest.mark.django_db
def test_user_is_only_required_field(user):
    ticket = WSAuthTicket.objects.create(user=user)


@pytest.mark.django_db
def test_not_expired(ticket):
    assert ticket.is_expired == False


@pytest.mark.django_db
def test_expired(ticket, settings):
    CHANNELS_WS_AUTH_EXPIRATION = getattr(
        settings,
        "CHANNELS_WS_AUTH_EXPIRATION",
        app_settings.CHANNELS_WS_AUTH_EXPIRATION,
    )
    ticket.created = timezone.now() - timedelta(seconds=CHANNELS_WS_AUTH_EXPIRATION + 1)
    assert ticket.is_expired == True
