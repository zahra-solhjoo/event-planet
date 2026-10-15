
from rest_framework.permissions import BasePermission


class IsOrganizer(BasePermission):
    message = "Only organizers can manage events."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "organizer"
        )
