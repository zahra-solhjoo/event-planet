
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event, EventAttribute, EventAttributeValue
from .serializers import EventSerializer
from .serializers import EventAttributeSerializer, EventAttributeValueSerializer

from django.shortcuts import get_object_or_404

from .permissions import IsOrganizer


class OrganizerEventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsOrganizer]

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class OrganizerEventStatusView(APIView):
    permission_classes = [IsOrganizer]

    def patch(self, request, pk):
        try:
            event = Event.objects.get(
                pk=pk,
                organizer=request.user,
            )
        except Event.DoesNotExist:
            return Response(
                {"detail": "Event not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        new_status = request.data.get("status")

        allowed_transitions = {
            Event.Status.DRAFT: [Event.Status.PUBLISHED],
            Event.Status.PUBLISHED: [
                Event.Status.CLOSED,
                Event.Status.FINISHED,
            ],
            Event.Status.CLOSED: [Event.Status.FINISHED],
            Event.Status.FINISHED: [],
        }

        if new_status not in allowed_transitions.get(event.status, []):
            return Response(
                {"detail": "Invalid status transition."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        event.status = new_status
        event.save(update_fields=["status", "updated_at"])

        return Response(EventSerializer(event).data)


class PublicEventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = []

    def get_queryset(self):
        return Event.objects.filter(status=Event.Status.PUBLISHED)


class PublicEventDetailView(generics.RetrieveAPIView):
    serializer_class = EventSerializer
    permission_classes = []

    def get_queryset(self):
        return Event.objects.filter(status=Event.Status.PUBLISHED)



class OrganizerEventAttributeListCreateView(generics.ListCreateAPIView):
    serializer_class = EventAttributeSerializer
    permission_classes = [IsOrganizer]

    def get_queryset(self):
        return EventAttribute.objects.filter(
            event_values__event__organizer=self.request.user,
        ).distinct()


class OrganizerEventAttributeValueListCreateView(generics.ListCreateAPIView):
    serializer_class = EventAttributeValueSerializer
    permission_classes = [IsOrganizer]

    def get_queryset(self):
        event_id = self.kwargs["event_id"]

        return EventAttributeValue.objects.filter(
            event_id=event_id,
            event__organizer=self.request.user,
        ).select_related("event", "attribute")

    def perform_create(self, serializer):
        event = get_object_or_404(
            Event,
            pk=self.kwargs["event_id"],
            organizer=self.request.user,
        )

        serializer.save(event=event)
