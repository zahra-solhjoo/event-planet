
from rest_framework import serializers

from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(
        source="registration.event.title",
        read_only=True,
    )
    registration = serializers.IntegerField(write_only=True)

    class Meta:
        model = Feedback
        fields = [
            "id",
            "registration",
            "event_title",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "event_title",
            "created_at",
        ]

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )
        return value

    def validate_registration(self, value):
        request = self.context["request"]

        from registrations.models import Registration

        registration = Registration.objects.filter(
            id=value,
            participant=request.user,
        ).first()

        if registration is None:
            raise serializers.ValidationError(
                "Registration not found for this user."
            )

        if hasattr(registration, "feedback"):
            raise serializers.ValidationError(
                "Feedback has already been submitted."
            )

        return value
