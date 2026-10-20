from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        PARTICIPANT = "participant", "Participant"
        ORGANIZER = "organizer", "Organizer"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PARTICIPANT,
    )

    def __str__(self):
        return self.username
