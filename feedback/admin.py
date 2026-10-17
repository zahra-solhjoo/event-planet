
from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "registration",
        "rating",
        "created_at",
    )
    list_filter = ("rating", "created_at")
    search_fields = (
        "registration__participant__username",
        "registration__event__title",
        "comment",
    )
    list_select_related = (
        "registration",
        "registration__participant",
        "registration__event",
    )
    readonly_fields = ("created_at",)
