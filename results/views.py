
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from events.models import Event
from events.permissions import IsOrganizer

from .models import EventResult
from .serializers import EventResultSerializer


class OrganizerEventResultView(generics.GenericAPIView):
    serializer_class = EventResultSerializer
    permission_classes = [IsOrganizer]

    def post(self, request, event_id):
        event = get_object_or_404(
            Event,
            pk=event_id,
            organizer=request.user,
        )

        if event.status != Event.Status.FINISHED:
            raise ValidationError(
                "Results can only be published for finished events."
            )

        result, created = EventResult.objects.get_or_create(
            event=event,
            defaults={
                "title": request.data.get("title", ""),
                "description": request.data.get("description", ""),
            },
        )

        if not created:
            raise ValidationError(
                "Results already exist for this event."
            )

        result.published = True
        result.save(update_fields=["published", "updated_at"])

        return Response(
            self.get_serializer(result).data,
            status=201,
        )


class PublicEventResultListView(generics.ListAPIView):
    serializer_class = EventResultSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return EventResult.objects.filter(
            published=True,
            event__status=Event.Status.FINISHED,
        ).select_related("event")


class PublicEventResultDetailView(generics.RetrieveAPIView):
    serializer_class = EventResultSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return EventResult.objects.filter(
            published=True,
            event__status=Event.Status.FINISHED,
        ).select_related("event")
