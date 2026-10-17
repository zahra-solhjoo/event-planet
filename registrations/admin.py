from django.contrib import admin

from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "participant",
        "event",
        "status",
        "registered_at",
    )
    list_filter = ("status", "event")
    search_fields = (
        "participant__username",
        "event__title",
    )
    list_select_related = ("participant", "event")
    ordering = ("-registered_at",)