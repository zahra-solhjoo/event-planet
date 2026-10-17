
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import Event
from .models import Registration
from .serializers import RegistrationSerializer


class EventRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        with transaction.atomic():
            event = get_object_or_404(
                Event.objects.select_for_update(),
                pk=event_id,
                status=Event.Status.PUBLISHED,
            )

            if request.user.role != "participant":
                raise ValidationError(
                    "Only participants can register for events."
                )

            existing_registration = Registration.objects.filter(
                participant=request.user,
                event=event,
            ).first()

            if existing_registration:
                raise ValidationError(
                    "You have already registered for this event."
                )

            registered_count = Registration.objects.filter(
                event=event,
                status=Registration.Status.REGISTERED,
            ).count()

            if registered_count >= event.capacity:
                raise ValidationError(
                    "This event has reached its capacity."
                )

            registration = Registration.objects.create(
                participant=request.user,
                event=event,
            )

        serializer = RegistrationSerializer(registration)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class MyRegistrationsView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event = get_object_or_404(
            Event,
            pk=self.kwargs["event_id"],
            organizer=self.request.user,
        )

        return Registration.objects.filter(
            event=event,
        ).select_related("event", "participant")

class OrganizerEventRegistrationsView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs["event_id"]

        return Registration.objects.filter(
            event_id=event_id,
            event__organizer=self.request.user,
        ).select_related("event", "participant")

    def list(self, request, *args, **kwargs):
        if request.user.role != "organizer":
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "Only organizers can view event participants."
            )

        return super().list(request, *args, **kwargs)