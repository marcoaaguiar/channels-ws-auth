from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/chat/open/", consumers.OpenChatConsumer),
    path("ws/chat/closed/", consumers.ClosedChatConsumer),
]
