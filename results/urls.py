from django.urls import path

from .views import (
    OrganizerEventResultView,
    PublicEventResultDetailView,
    PublicEventResultListView,
)


urlpatterns = [
    path(
        "organizer/events/<int:event_id>/results/",
        OrganizerEventResultView.as_view(),
        name="organizer-event-result",
    ),
    path(
        "results/",
        PublicEventResultListView.as_view(),
        name="public-result-list",
    ),
    path(
        "results/<int:pk>/",
        PublicEventResultDetailView.as_view(),
        name="public-result-detail",
    ),
]