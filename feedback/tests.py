
from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User
from events.models import Event
from registrations.models import Registration
from feedback.models import Feedback


class FeedbackTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.organizer = User.objects.create_user(
            username="feedback_organizer",
            password="TestPass123!",
            role=User.Role.ORGANIZER,
        )

        self.participant = User.objects.create_user(
            username="feedback_participant",
            password="TestPass123!",
            role=User.Role.PARTICIPANT,
        )

        self.event = Event.objects.create(
            title="Finished Workshop",
            description="Workshop for feedback tests",
            start_at="2026-11-15T09:00:00Z",
            end_at="2026-11-15T12:00:00Z",
            capacity=10,
            organizer=self.organizer,
            status=Event.Status.FINISHED,
        )

        self.registration = Registration.objects.create(
            participant=self.participant,
            event=self.event,
        )

        self.client.force_authenticate(user=self.participant)
        self.url = "/api/feedback/"

    def test_registered_participant_can_submit_feedback(self):
        response = self.client.post(
            self.url,
            {
                "registration": self.registration.id,
                "rating": 5,
                "comment": "Great workshop!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Feedback.objects.count(), 1)
    def test_feedback_rejects_rating_above_five(self):
        response = self.client.post(
            self.url,
            {
                "registration": self.registration.id,
                "rating": 6,
                "comment": "Invalid rating",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Feedback.objects.count(), 0)
    def test_duplicate_feedback_is_rejected(self):
        Feedback.objects.create(
            registration=self.registration,
            rating=5,
            comment="First review",
        )

        response = self.client.post(
            self.url,
            {
                "registration": self.registration.id,
                "rating": 4,
                "comment": "Second review",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Feedback.objects.count(), 1)

    def test_feedback_is_rejected_for_unfinished_event(self):
        self.event.status = Event.Status.PUBLISHED
        self.event.save()

        response = self.client.post(
            self.url,
            {
                "registration": self.registration.id,
                "rating": 5,
                "comment": "Too early",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Feedback.objects.count(), 0)
    def test_feedback_rejected_for_another_participants_registration(self):
        other_participant = User.objects.create_user(
            username="another_feedback_participant",
            password="TestPass123!",
            role=User.Role.PARTICIPANT,
        )

        other_registration = Registration.objects.create(
            participant=other_participant,
            event=self.event,
        )

        response = self.client.post(
            self.url,
            {
                "registration": other_registration.id,
                "rating": 5,
                "comment": "Unauthorized feedback",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Feedback.objects.count(), 0)
    def test_organizer_cannot_submit_feedback(self):
        self.client.force_authenticate(user=self.organizer)

        response = self.client.post(
            self.url,
            {
                "registration": self.registration.id,
                "rating": 5,
                "comment": "Organizer feedback",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Feedback.objects.count(), 0)