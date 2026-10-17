from django.urls import path

from .views import (
    EventRegistrationView,
    MyRegistrationsView,
    OrganizerEventRegistrationsView,
)


urlpatterns = [
    path(
        "events/<int:event_id>/register/",
        EventRegistrationView.as_view(),
        name="event-register",
    ),
    path(
        "my-registrations/",
        MyRegistrationsView.as_view(),
        name="my-registrations",
    ),
    path(
        "organizer/events/<int:event_id>/registrations/",
        OrganizerEventRegistrationsView.as_view(),
        name="organizer-event-registrations",
    ),
]