from django.conf import settings
from django.db import models


class Event(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        CLOSED = "closed", "Closed"
        FINISHED = "finished", "Finished"

    title = models.CharField(max_length=200)
    description = models.TextField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_events",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_at"]

    def __str__(self):
        return self.title


class EventStage(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="stages",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["event", "order"],
                name="unique_event_stage_order",
            ),
        ]

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.end_at <= self.start_at:
            raise ValidationError(
                "Stage end time must be later than start time."
            )

    def __str__(self):
        return f"{self.event.title} - {self.title}"

class EventStageRole(models.Model):
    class Role(models.TextChoices):
        SPEAKER = "speaker", "Speaker"
        JUDGE = "judge", "Judge"
        COACH = "coach", "Coach"

    stage = models.ForeignKey(
        EventStage,
        on_delete=models.CASCADE,
        related_name="stage_roles",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="event_stage_roles",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["stage", "user", "role"],
                name="unique_event_stage_user_role",
            ),
        ]

    def __str__(self):
        return f"{self.stage.title} - {self.user.username} - {self.role}"

class EventAttribute(models.Model):
    class DataType(models.TextChoices):
        TEXT = "text", "Text"
        INTEGER = "integer", "Integer"
        DECIMAL = "decimal", "Decimal"
        BOOLEAN = "boolean", "Boolean"

    name = models.CharField(max_length=100)
    data_type = models.CharField(
        max_length=20,
        choices=DataType.choices,
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class EventAttributeValue(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="attribute_values",
    )
    attribute = models.ForeignKey(
        EventAttribute,
        on_delete=models.CASCADE,
        related_name="event_values",
    )

    text_value = models.TextField(null=True, blank=True)
    integer_value = models.BigIntegerField(null=True, blank=True)
    decimal_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    boolean_value = models.BooleanField(null=True, blank=True)
    
    def clean(self):
        from django.core.exceptions import ValidationError

        value_fields = {
            EventAttribute.DataType.TEXT: self.text_value,
            EventAttribute.DataType.INTEGER: self.integer_value,
            EventAttribute.DataType.DECIMAL: self.decimal_value,
            EventAttribute.DataType.BOOLEAN: self.boolean_value,
        }

        current_value = value_fields.get(self.attribute.data_type)

        populated_fields = [
            value
            for value in [
                self.text_value,
                self.integer_value,
                self.decimal_value,
                self.boolean_value,
            ]
            if value is not None
        ]

        if len(populated_fields) != 1 or current_value is None:
            raise ValidationError(
                "Provide exactly one value matching the attribute data type."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "attribute"],
                name="unique_event_attribute_value",
            ),
        ]

    def __str__(self):
        return f"{self.event.title} - {self.attribute.name}"
