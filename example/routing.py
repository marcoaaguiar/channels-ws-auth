from channels.routing import ProtocolTypeRouter, URLRouter
from channels_ws_auth.middleware import WSAuthMiddleware
from example.chat import routing

application = ProtocolTypeRouter(
    {"websocket": WSAuthMiddleware(URLRouter(routing.websocket_urlpatterns)),}
)
