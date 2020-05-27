import json
from channels.generic.websocket import WebsocketConsumer
from channels_ws_auth.utils import is_authenticated


class OpenChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(
            text_data=json.dumps(
                {"message": (f"Connected to {self.__class__.__name__}")}
            )
        )

    def disconnect(self, close_code):
        self.send(text_data=json.dumps({"message": ("Disconnected")}))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        user = self.scope["user"]
        username = "Anonymous" if user.is_anonymous else user.username

        message = f'{username} said: {text_data_json["message"]}'
        self.send(text_data=json.dumps({"message": message}))


@is_authenticated
class ClosedChatConsumer(OpenChatConsumer):
    pass
