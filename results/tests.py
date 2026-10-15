
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
