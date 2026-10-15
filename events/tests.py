
from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from events.models import Event


class OrganizerEventPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.organizer = User.objects.create_user(
            username="event_organizer",
            password="TestPass123!",
            role=User.Role.ORGANIZER,
        )

        self.other_organizer = User.objects.create_user(
            username="other_organizer",
            password="TestPass123!",
            role=User.Role.ORGANIZER,
        )

        self.participant = User.objects.create_user(
            username="event_participant",
            password="TestPass123!",
            role=User.Role.PARTICIPANT,
        )

        self.event = Event.objects.create(
            title="Organizer Workshop",
            description="Permission test",
            start_at="2026-11-15T09:00:00Z",
            end_at="2026-11-15T12:00:00Z",
            capacity=20,
            organizer=self.organizer,
            status=Event.Status.DRAFT,
        )

        self.url = "/api/organizer/events/"

    def test_organizer_sees_only_own_events(self):
        Event.objects.create(
            title="Other Workshop",
            description="Another organizer's event",
            start_at="2026-11-16T09:00:00Z",
            end_at="2026-11-16T12:00:00Z",
            capacity=20,
            organizer=self.other_organizer,
            status=Event.Status.DRAFT,
        )

        self.client.force_authenticate(user=self.organizer)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["title"],
            "Organizer Workshop",
        )

    def test_participant_cannot_manage_events(self):
        self.client.force_authenticate(user=self.participant)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_unauthenticated_user_cannot_manage_events(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)
