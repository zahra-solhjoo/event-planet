from rest_framework import serializers

from .models import EventResult


class EventResultSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(
        source="event.title",
        read_only=True,
    )

    class Meta:
        model = EventResult
        fields = [
            "id",
            "event",
            "event_title",
            "title",
            "description",
            "published",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "event",
            "event_title",
            "published",
            "created_at",
            "updated_at",
        ]