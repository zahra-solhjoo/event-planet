
from rest_framework import serializers

from .models import Event, EventAttribute, EventAttributeValue, EventStage

class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source="organizer.username")

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "start_at",
            "end_at",
            "capacity",
            "organizer",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "organizer",
            "status",
            "event",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        start_at = attrs.get(
            "start_at",
            getattr(self.instance, "start_at", None),
        )
        end_at = attrs.get(
            "end_at",
            getattr(self.instance, "end_at", None),
        )

        if start_at and end_at and end_at <= start_at:
            raise serializers.ValidationError(
                "End time must be later than start time."
            )

        return attrs

class EventAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAttribute
        fields = ["id", "name", "data_type", "description"]

class EventAttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(
        source="attribute.name",
        read_only=True,
    )
    data_type = serializers.CharField(
        source="attribute.data_type",
        read_only=True,
    )

    class Meta:
        model = EventAttributeValue
        fields = [
            "id",
            "event",
            "attribute",
            "attribute_name",
            "data_type",
            "text_value",
            "integer_value",
            "decimal_value",
            "boolean_value",
        ]
        read_only_fields = [
            "id",
            "event",
            "attribute_name",
            "data_type",
        ]

    def validate(self, attrs):
        attribute = attrs.get("attribute")

        if attribute is None:
            raise serializers.ValidationError({
                "attribute": "انتخاب ویژگی الزامی است."
            })

        value_fields = [
            "text_value",
            "integer_value",
            "decimal_value",
            "boolean_value",
        ]

        supplied_values = [
            field
            for field in value_fields
            if attrs.get(field) is not None
        ]

        expected_field = {
            "text": "text_value",
            "integer": "integer_value",
            "decimal": "decimal_value",
            "boolean": "boolean_value",
        }.get(attribute.data_type)

        if expected_field is None:
            raise serializers.ValidationError(
                "نوع ویژگی معتبر نیست."
            )

        if (
            len(supplied_values) != 1
            or supplied_values[0] != expected_field
        ):
            raise serializers.ValidationError({
                "value": (
                    f"برای این ویژگی فقط فیلد "
                    f"{expected_field} را با مقدار مناسب ارسال کن."
                )
            })

        event_id = self.context["view"].kwargs.get("event_id")

        duplicate = EventAttributeValue.objects.filter(
            event_id=event_id,
            attribute=attribute,
        ).exists()

        if duplicate:
            raise serializers.ValidationError({
                "attribute": (
                    "برای این ویژگی در این رویداد قبلاً مقدار ثبت شده است."
                )
            })

        return attrs

class EventStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventStage
        fields = [
            "id",
            "event",
            "title",
            "description",
            "order",
            "start_at",
            "end_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id","event", "created_at", "updated_at"]

    def validate(self, attrs):
        start_at = attrs.get(
            "start_at",
            getattr(self.instance, "start_at", None),
        )
        end_at = attrs.get(
            "end_at",
            getattr(self.instance, "end_at", None),
        )

        if start_at and end_at and end_at <= start_at:
            raise serializers.ValidationError(
                "Stage end time must be later than start time."
            )

        return attrs        