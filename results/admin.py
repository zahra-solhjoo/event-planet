
from django.contrib import admin

from .models import EventResult


@admin.register(EventResult)
class EventResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "event",
        "published",
        "created_at",
        "updated_at",
    )
    list_filter = ("published", "created_at")
    search_fields = (
        "title",
        "description",
        "event__title",
    )
    list_select_related = ("event",)
    readonly_fields = ("created_at", "updated_at")
