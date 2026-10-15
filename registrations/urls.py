
from django.urls import path

from .views import EventRegistrationView, MyRegistrationsView


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
]
