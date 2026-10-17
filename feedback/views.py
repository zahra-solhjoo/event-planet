
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from events.permissions import IsParticipant, IsOrganizer

from events.models import Event
from registrations.models import Registration

from .models import Feedback
from .serializers import FeedbackSerializer


class FeedbackListCreateView(generics.ListCreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsParticipant]

    def get_queryset(self):
        return Feedback.objects.filter(
            registration__participant=self.request.user
        ).select_related(
            "registration__event",
            "registration__participant",
        )

    def perform_create(self, serializer):
        from registrations.models import Registration

        registration_id = serializer.validated_data["registration"]

        registration = Registration.objects.filter(
            id=registration_id,
            participant=self.request.user,
        ).first()

        if registration is None:
            raise ValidationError(
                "Registration not found for the current participant."
            )

        if registration.event.status != Event.Status.FINISHED:
            raise ValidationError(
                "Feedback is allowed only for finished events."
            )

        if registration.status != Registration.Status.REGISTERED:
            raise ValidationError(
                "Only active registrations can submit feedback."
            )
        serializer.save(registration=registration)

class OrganizerEventFeedbackListView(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsOrganizer]

    def get_queryset(self):
        return Feedback.objects.filter(
            registration__event__organizer=self.request.user,
            registration__event_id=self.kwargs["event_id"],
        ).select_related(
            "registration__event",
            "registration__participant",
        )