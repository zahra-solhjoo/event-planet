
from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from events.models import Event
from registrations.models import Registration


class EventRegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.participant = User.objects.create_user(
            username="test_participant",
            password="TestPass123!",
            role=User.Role.PARTICIPANT,
        )

        self.organizer = User.objects.create_user(
            username="test_organizer",
            password="TestPass123!",
            role=User.Role.ORGANIZER,
        )

        self.event = Event.objects.create(
            title="Test Workshop",
            description="Workshop for testing",
            start_at="2026-11-15T09:00:00Z",
            end_at="2026-11-15T12:00:00Z",
            capacity=1,
            organizer=self.organizer,
            status=Event.Status.PUBLISHED,
        )

        self.client.force_authenticate(user=self.participant)
        self.url = f"/api/registrations/events/{self.event.id}/register/"

    def test_participant_can_register(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Registration.objects.count(), 1)

    def test_duplicate_registration_is_rejected(self):
        Registration.objects.create(
            participant=self.participant,
            event=self.event,
        )

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Registration.objects.count(), 1)

    def test_registration_fails_when_event_is_full(self):
        another_participant = User.objects.create_user(
            username="another_participant",
            password="TestPass123!",
            role=User.Role.PARTICIPANT,
        )

        Registration.objects.create(
            participant=another_participant,
            event=self.event,
        )

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Registration.objects.count(), 1)
class OrganizerEventRegistrationsTests(TestCase):
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
            description="Testing participant list",
            start_at="2026-11-15T09:00:00Z",
            end_at="2026-11-15T12:00:00Z",
            capacity=10,
            organizer=self.organizer,
            status=Event.Status.PUBLISHED,
        )

        self.registration = Registration.objects.create(
            participant=self.participant,
            event=self.event,
        )

        self.url = (
            f"/api/registrations/organizer/events/"
            f"{self.event.id}/registrations/"
        )

    def test_organizer_can_view_own_event_participants(self):
        self.client.force_authenticate(user=self.organizer)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_other_organizer_cannot_view_event_participants(self):
        self.client.force_authenticate(user=self.other_organizer)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_participant_cannot_view_organizer_participant_list(self):
        self.client.force_authenticate(user=self.participant)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)