from rest_framework import serializers
from .models import WSAuthTicket


class WSAuthTicketSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    ticket = serializers.UUIDField(
        read_only=True,
        required=False,
        source="key",
        help_text="Ticket to be used to open a WebSocket Connection",
    )

    class Meta:
        model = WSAuthTicket
        fields = ["user", "ticket"]
