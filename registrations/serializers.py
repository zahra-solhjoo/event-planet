
from rest_framework import serializers

from .models import Registration


class RegistrationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(
        source="event.title",
        read_only=True,
    )
    participant = serializers.CharField(
        source="participant.username",
        read_only=True,
    )

    class Meta:
        model = Registration
        fields = [
            "id",
            "event",
            "event_title",
            "participant",
            "status",
            "registered_at",
        ]
        read_only_fields = [
            "id",
            "event_title",
            "participant",
            "status",
            "registered_at",
        ]
