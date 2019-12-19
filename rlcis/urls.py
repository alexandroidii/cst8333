from django.contrib import admin
from django.urls import (
    include, path, reverse,
)
from . import views

""" 
RLCIS Urls to direct navigation through the app 

App Namespace: 'rlcis'

Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19
"""


app_name = 'rlcis'
urlpatterns = [
    
    # root path for the home page
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
    #return a list of incidents
    path(
        'incidents/',
        views.incidents,
        name='incidents'),
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
    # return a list of Scenarios
    path(
        'scenarios/',
        views.scenarios,
        name='scenarios'),
]
