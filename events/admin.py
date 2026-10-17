from django.contrib import admin

from .models import (
    Event,
    EventStage,
    EventStageRole,
    EventAttribute,
    EventAttributeValue,
)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "organizer",
        "status",
        "start_at",
        "end_at",
        "capacity",
    )
    list_filter = ("status",)
    search_fields = ("title", "description")
    list_select_related = ("organizer",)


@admin.register(EventStage)
class EventStageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "event",
        "order",
        "start_at",
        "end_at",
    )
    list_filter = ("event",)
    search_fields = ("title", "event__title")
    list_select_related = ("event",)


@admin.register(EventAttribute)
class EventAttributeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "data_type")
    list_filter = ("data_type",)
    search_fields = ("name", "description")


@admin.register(EventAttributeValue)
class EventAttributeValueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event",
        "attribute",
        "text_value",
        "integer_value",
        "decimal_value",
        "boolean_value",
    )
    list_filter = ("attribute",)
    search_fields = ("event__title", "attribute__name")
    list_select_related = ("event", "attribute")

@admin.register(EventStageRole)
class EventStageRoleAdmin(admin.ModelAdmin):
    list_display = ("id", "stage", "user", "role")
    list_filter = ("role", "stage__event")
    search_fields = (
        "stage__title",
        "stage__event__title",
        "user__username",
    )
    list_select_related = ("stage", "stage__event", "user")