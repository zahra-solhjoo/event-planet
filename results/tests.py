
from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from events.models import Event
from results.models import EventResult


class PublicEventResultTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.organizer = User.objects.create_user(
            username="test_organizer",
            password="TestPass123!",
            role=User.Role.ORGANIZER,
        )

        self.event = Event.objects.create(
            title="Test Event",
            description="Event for testing",
            start_at="2026-11-15T09:00:00Z",
            end_at="2026-11-15T12:00:00Z",
            capacity=20,
            organizer=self.organizer,
            status=Event.Status.FINISHED,
        )

        self.result = EventResult.objects.create(
            event=self.event,
            title="Test Results",
            description="Public test result",
            published=True,
        )

    def test_published_results_are_public(self):
        response = self.client.get("/api/results/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["title"],
            "Test Results",
        )

    def test_unpublished_results_are_hidden(self):
        self.result.published = False
        self.result.save()

        response = self.client.get("/api/results/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)


    def test_organizer_cannot_publish_results_for_another_organizers_event(self):
        other_organizer = User.objects.create_user(
            username="other_organizer",
            password="TestPass123!",
            role=User.Role.ORGANIZER,
        )
        other_event = Event.objects.create(
            title="Another Event",
            description="Owned by another organizer",
            start_at="2026-11-16T09:00:00Z",
            end_at="2026-11-16T12:00:00Z",
            capacity=20,
            organizer=other_organizer,
            status=Event.Status.FINISHED,
        )

        self.client.force_authenticate(user=self.organizer)
        response = self.client.post(
            f"/api/organizer/events/{other_event.id}/results/",
            {
                "title": "Unauthorized Results",
                "description": "Should not be published",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(
            EventResult.objects.filter(event=other_event).exists()
        )

    def test_results_cannot_be_published_before_event_finishes(self):
        self.event.status = Event.Status.PUBLISHED
        self.event.save()

        self.client.force_authenticate(user=self.organizer)
        response = self.client.post(
            f"/api/organizer/events/{self.event.id}/results/",
            {
                "title": "Premature Results",
                "description": "Should not be published yet",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(
            EventResult.objects.filter(
                event=self.event,
                title="Premature Results",
            ).exists()
        )
