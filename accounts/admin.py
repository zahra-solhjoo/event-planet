
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "role",
        "is_staff",
        "is_active",
    )
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )
    ordering = ("username",)

    fieldsets = UserAdmin.fieldsets + (
        ("Event Planet", {"fields": ("role",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Event Planet", {"fields": ("role",)}),
    )
