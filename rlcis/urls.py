from django.urls import path

from rlcis.views import (IncidentCreate, IncidentDelete, IncidentDetails,
                         IncidentList, IncidentUpdate)

urlpatterns = [
    path(
        '',
        IncidentList.as_view(),
        name="incident-list"),
    path(
        '<pk>/',
        IncidentDetails.as_view(),
        name='incident-details'),
    path(
        'incident/add/',
        IncidentCreate.as_view(),
        name='incident-add'),
    path(
        'incident/<int:pk>/',
        IncidentUpdate.as_view(),
        name='incident-update'),
    path(
        'incident/<int:pk>/delete/',
        IncidentDelete.as_view(),
        name='incident-delete'),
]
