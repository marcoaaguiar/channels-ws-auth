from rest_framework import serializers
from .models import WSAuthTicket


class WSAuthTicketSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    key = serializers.UUIDField(
        read_only=True,
        required=False,
        help_text="Key to used to open WebSocket Connection",
    )

    class Meta:
        model = WSAuthTicket
        fields = ["user", "key"]
