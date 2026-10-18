
from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import User


class AccountAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/accounts/register/"
        self.login_url = "/api/accounts/login/"

    def test_user_can_register(self):
        response = self.client.post(
            self.register_url,
            {
                "username": "new_participant",
                "email": "participant@example.com",
                "password": "TestPass123!",
                "role": "participant",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            User.objects.filter(username="new_participant").exists()
        )
    def test_user_cannot_register_as_organizer(self):
        response = self.client.post(
            self.register_url,
            {
                "username": "fake_organizer",
                "email": "organizer@example.com",
                "password": "TestPass123!",
                "role": "organizer",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        user = User.objects.get(username="fake_organizer")
        self.assertEqual(user.role, User.Role.PARTICIPANT)
    def test_user_can_login_and_receive_token(self):
        User.objects.create_user(
            username="login_participant",
            password="TestPass123!",
            role=User.Role.PARTICIPANT,
        )

        response = self.client.post(
            self.login_url,
            {
                "username": "login_participant",
                "password": "TestPass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
        self.assertEqual(
            response.data["role"],
            User.Role.PARTICIPANT,
        )
