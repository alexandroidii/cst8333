from django.urls import include, path

from . import views

app_name = 'rlcis'
urlpatterns = [
    path(
        '',
        views.index,
        name='home'),
    path(
        'add/',
        views.incident_form,
        name="incident_insert"),
    path(
        '<int:id>/',
        views.incident_form,
        name='incident_update'),
    path(
        'delete/<int:id>/',
        views.incident_delete,
        name='incident_delete'),
    path(
        'list/',
        views.incident_list,
        name='incident_list'),
    path(
        'scenarios/',
        views.scenarios,
        name='scenarios'),
    path(
        'searchIncidents/',
        views.searchIncidents,
        name='search_incidents'),
]
