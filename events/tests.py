
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

class OrganizerEventStatusTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.organizer = User.objects.create_user(
            username="status_organizer",
            password="TestPass123!",
            role=User.Role.ORGANIZER,
        )

        self.other_organizer = User.objects.create_user(
            username="other_status_organizer",
            password="TestPass123!",
            role=User.Role.ORGANIZER,
        )

        self.event = Event.objects.create(
            title="Status Test Event",
            description="Testing event status transitions",
            start_at="2026-11-15T09:00:00Z",
            end_at="2026-11-15T12:00:00Z",
            capacity=20,
            organizer=self.organizer,
            status=Event.Status.DRAFT,
        )

        self.url = (
            f"/api/organizer/events/{self.event.id}/status/"
        )
        self.client.force_authenticate(user=self.organizer)

    def test_draft_can_be_published(self):
        response = self.client.patch(
            self.url,
            {"status": Event.Status.PUBLISHED},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.event.refresh_from_db()
        self.assertEqual(
            self.event.status,
            Event.Status.PUBLISHED,
        )

    def test_draft_cannot_be_finished_directly(self):
        response = self.client.patch(
            self.url,
            {"status": Event.Status.FINISHED},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.event.refresh_from_db()
        self.assertEqual(self.event.status, Event.Status.DRAFT)

    def test_finished_event_cannot_be_reopened(self):
        self.event.status = Event.Status.FINISHED
        self.event.save()

        response = self.client.patch(
            self.url,
            {"status": Event.Status.PUBLISHED},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_organizer_cannot_change_another_organizers_event(self):
        other_event = Event.objects.create(
            title="Another Event",
            description="Owned by another organizer",
            start_at="2026-11-16T09:00:00Z",
            end_at="2026-11-16T12:00:00Z",
            capacity=20,
            organizer=self.other_organizer,
            status=Event.Status.DRAFT,
        )

        response = self.client.patch(
            f"/api/organizer/events/{other_event.id}/status/",
            {"status": Event.Status.PUBLISHED},
            format="json",
        )

        self.assertEqual(response.status_code, 404)

from events.models import EventAttribute, EventAttributeValue


class DynamicEventAttributeTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.organizer = User.objects.create_user(
            username="attribute_organizer",
            password="TestPass123!",
            role=User.Role.ORGANIZER,
        )

        self.event = Event.objects.create(
            title="Dynamic Attribute Event",
            description="Testing dynamic attributes",
            start_at="2026-11-15T09:00:00Z",
            end_at="2026-11-15T12:00:00Z",
            capacity=20,
            organizer=self.organizer,
            status=Event.Status.DRAFT,
        )

        self.url = (
            f"/api/organizer/events/{self.event.id}/attributes/"
        )
        self.client.force_authenticate(user=self.organizer)

    def test_organizer_can_create_attribute(self):
        response = self.client.post(
            self.url,
            {
                "name": "Difficulty",
                "data_type": "text",
                "description": "Workshop difficulty",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            EventAttribute.objects.filter(name="Difficulty").exists()
        )

    def test_attribute_definitions_are_independent(self):
        attribute = EventAttribute.objects.create(
            name="Platform",
            data_type=EventAttribute.DataType.TEXT,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            attribute.id,
            [item["id"] for item in response.data],
        )

    def test_attribute_value_must_match_data_type(self):
        attribute = EventAttribute.objects.create(
            name="Number of rounds",
            data_type=EventAttribute.DataType.INTEGER,
        )

        value_url = (
            f"/api/organizer/events/{self.event.id}/attribute-values/"
        )

        response = self.client.post(
            value_url,
            {
                "attribute": attribute.id,
                "text_value": "three",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(EventAttributeValue.objects.count(), 0)

    def test_organizer_cannot_add_attribute_value_to_another_organizers_event(self):
        other_organizer = User.objects.create_user(
            username="other_attribute_organizer",
            password="TestPass123!",
            role=User.Role.ORGANIZER,
        )

        other_event = Event.objects.create(
            title="Other Organizer Event",
            description="An event owned by someone else",
            start_at="2026-11-16T09:00:00Z",
            end_at="2026-11-16T12:00:00Z",
            capacity=20,
            organizer=other_organizer,
            status=Event.Status.DRAFT,
        )

        attribute = EventAttribute.objects.create(
            name="Security Test",
            data_type=EventAttribute.DataType.TEXT,
        )

        value_url = (
            f"/api/organizer/events/{other_event.id}/attribute-values/"
        )

        response = self.client.post(
            value_url,
            {
                "attribute": attribute.id,
                "text_value": "Unauthorized value",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(
            EventAttributeValue.objects.filter(
                event=other_event,
                attribute=attribute,
            ).exists()
        )

class SharedDynamicAttributeTests(TestCase):
    def setUp(self):
        self.organizer = User.objects.create_user(
            username="shared_attribute_organizer",
            password="TestPass123!",
            role=User.Role.ORGANIZER,
        )

        self.event_one = Event.objects.create(
            title="First Event",
            description="First event",
            start_at="2026-11-15T09:00:00Z",
            end_at="2026-11-15T12:00:00Z",
            capacity=20,
            organizer=self.organizer,
        )

        self.event_two = Event.objects.create(
            title="Second Event",
            description="Second event",
            start_at="2026-11-16T09:00:00Z",
            end_at="2026-11-16T12:00:00Z",
            capacity=20,
            organizer=self.organizer,
        )

        self.attribute = EventAttribute.objects.create(
            name="Platform",
            data_type=EventAttribute.DataType.TEXT,
        )

    def test_attribute_can_be_shared_between_events(self):
        first_value = EventAttributeValue.objects.create(
            event=self.event_one,
            attribute=self.attribute,
            text_value="Zoom",
        )

        second_value = EventAttributeValue.objects.create(
            event=self.event_two,
            attribute=self.attribute,
            text_value="Google Meet",
        )

        self.assertEqual(
            EventAttributeValue.objects.filter(
                attribute=self.attribute,
            ).count(),
            2,
        )

        first_value.refresh_from_db()
        second_value.refresh_from_db()

        self.assertEqual(first_value.text_value, "Zoom")
        self.assertEqual(second_value.text_value, "Google Meet")

    def test_duplicate_attribute_value_for_event_is_rejected(self):
        EventAttributeValue.objects.create(
            event=self.event_one,
            attribute=self.attribute,
            text_value="Zoom",
        )

        with self.assertRaises(Exception):
            EventAttributeValue.objects.create(
                event=self.event_one,
                attribute=self.attribute,
                text_value="Google Meet",
            )