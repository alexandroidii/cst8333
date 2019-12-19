from django.contrib import admin
from django.urls import (
    include, path, reverse,
)
from . import views

app_name = 'rlcis'
urlpatterns = [
    
    path(
        '',
        views.index,
        name='home'),
    path(
        'add_incident/',
        views.incident_form,
        name="incident_insert"),
    path(
        'incident<int:id>/',
        views.incident_form,
        name='incident_update'),
    path(
        'delete_incident/<int:id>/',
        views.incident_delete,
        name='incident_delete'),
    path(
        'incidents/',
        views.incident_list,
        name='incident_list'),
    path(
        'search_incidents/',
        views.incident_search,
        name='incident_search'),
    path(
        'scenarios/',
        views.scenario_list,
        name='scenario_list'),
    path(
        'add_scenario/',
        views.scenario_form,
        name='scenario_insert'),
    path(
        'scenario<int:id>/',
        views.scenario_form,
        name='scenario_update'),
    path(
        'delete_scenario/<int:id>/',
        views.scenario_delete,
        name='scenario_delete'),
]
