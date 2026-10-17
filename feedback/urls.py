from django.urls import path

from .views import (
    FeedbackListCreateView,
    OrganizerEventFeedbackListView,
)


urlpatterns = [
    path("", FeedbackListCreateView.as_view(), name="feedback-list-create"),
    path(
        "organizer/events/<int:event_id>/feedback/",
        OrganizerEventFeedbackListView.as_view(),
        name="organizer-event-feedback",
    ),
]