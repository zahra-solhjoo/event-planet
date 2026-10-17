
from django.urls import path
from .views import (
    OrganizerEventListCreateView,
    OrganizerEventStatusView,
    PublicEventDetailView,
    PublicEventListView,
    OrganizerEventAttributeListCreateView,
    OrganizerEventAttributeValueListCreateView,
    OrganizerEventStageListCreateView,
    OrganizerEventStageDetailView,
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
    path(
        "organizer/events/<int:event_id>/stages/",
        OrganizerEventStageListCreateView.as_view(),
        name="organizer-event-stages",
    ),
    path(
        "organizer/events/<int:event_id>/stages/<int:stage_id>/",
        OrganizerEventStageDetailView.as_view(),
        name="organizer-event-stage-detail",
    ),

]
