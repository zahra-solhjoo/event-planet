
from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from events.models import Event, EventStage


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


from datetime import timedelta

from django.utils import timezone


class OrganizerEventStageTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.organizer = User.objects.create_user(
            username="stage_organizer",
            password="TestPass123!",
            role=User.Role.ORGANIZER,
        )

        self.other_organizer = User.objects.create_user(
            username="other_stage_organizer",
            password="TestPass123!",
            role=User.Role.ORGANIZER,
        )

        self.participant = User.objects.create_user(
            username="stage_participant",
            password="TestPass123!",
            role=User.Role.PARTICIPANT,
        )

        now = timezone.now()

        self.event = Event.objects.create(
            title="Stage Test Event",
            description="Event for stage tests",
            start_at=now + timedelta(days=2),
            end_at=now + timedelta(days=3),
            capacity=20,
            organizer=self.organizer,
            status=Event.Status.DRAFT,
        )

        self.other_event = Event.objects.create(
            title="Other Stage Event",
            description="Another organizer's event",
            start_at=now + timedelta(days=4),
            end_at=now + timedelta(days=5),
            capacity=20,
            organizer=self.other_organizer,
            status=Event.Status.DRAFT,
        )

        self.stage = EventStage.objects.create(
            event=self.event,
            title="Introduction",
            description="Opening session",
            order=1,
            start_at=self.event.start_at,
            end_at=self.event.start_at + timedelta(hours=1),
        )

        self.list_url = (
            f"/api/organizer/events/{self.event.id}/stages/"
        )

        self.detail_url = (
            f"/api/organizer/events/{self.event.id}/"
            f"stages/{self.stage.id}/"
        )

    def test_organizer_can_list_own_event_stages(self):
        self.client.force_authenticate(user=self.organizer)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["title"],
            "Introduction",
        )

    def test_organizer_can_create_stage(self):
        self.client.force_authenticate(user=self.organizer)

        response = self.client.post(
            self.list_url,
            {
                "title": "Main Workshop",
                "description": "Workshop session",
                "order": 2,
                "start_at": (
                    self.event.start_at + timedelta(hours=2)
                ).isoformat(),
                "end_at": (
                    self.event.start_at + timedelta(hours=3)
                ).isoformat(),
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(EventStage.objects.count(), 2)

    def test_organizer_cannot_access_another_organizers_stages(self):
        self.client.force_authenticate(user=self.organizer)

        other_stage = EventStage.objects.create(
            event=self.other_event,
            title="Private Stage",
            description="Another organizer's stage",
            order=1,
            start_at=self.other_event.start_at,
            end_at=(
                self.other_event.start_at + timedelta(hours=1)
            ),
        )

        response = self.client.get(
            f"/api/organizer/events/{self.other_event.id}/"
            f"stages/{other_stage.id}/"
        )

        self.assertEqual(response.status_code, 404)

    def test_participant_cannot_manage_stages(self):
        self.client.force_authenticate(user=self.participant)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 403)
