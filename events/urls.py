
from django.urls import path
from .views import (
    OrganizerEventListCreateView,
    OrganizerEventStatusView,
    PublicEventDetailView,
    PublicEventListView,
    OrganizerEventAttributeListCreateView,
    OrganizerEventAttributeValueListCreateView,
)


urlpatterns = [
    path(
        "organizer/events/",
        OrganizerEventListCreateView.as_view(),
        name="organizer-event-list-create",
    ),
    path(
        "events/",
        PublicEventListView.as_view(),
        name="public-event-list",
    ),
    path(
        "events/<int:pk>/",
        PublicEventDetailView.as_view(),
        name="public-event-detail",
    ),
    path(
        "organizer/events/<int:pk>/status/",
        OrganizerEventStatusView.as_view(),
    ),

    path(
        "organizer/events/<int:event_id>/attributes/",
        OrganizerEventAttributeListCreateView.as_view(),
        name="organizer-event-attributes",
    ),
    path(
        "organizer/events/<int:event_id>/attribute-values/",
        OrganizerEventAttributeValueListCreateView.as_view(),
        name="organizer-event-attribute-values",
    ),

]
