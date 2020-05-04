# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import RequestWSTicketView

app_name = "channels_ws_auth"
urlpatterns = [url(r"", RequestWSTicketView.as_view())]
