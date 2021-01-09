from django.contrib import admin
from django.urls import (
    include, path, reverse,
)
from django.conf import settings
from django.conf.urls.static import static

from . import views

""" 
RLCIS Urls to direct navigation through the app - all application views 
are imported.

App Namespace: 'rlcis'

Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19
"""


app_name = 'rlcis'
urlpatterns = [

    # root path for the home page
    path('', views.index, name='home'),
    # path(
    #     'upload/',
    #     views.upload,
    #     name='upload'),
    path(
        'documents/',
        views.document_list,
        name='document_list'),
    path(
        'documents/upload/',
        views.upload_document,
        name='upload_document'),
    path(
        'class/documents/', 
        views.DocumentListView.as_view(), 
        name='class_document_list'),
    path(
        'class/documents/upload', 
        views.UploadDocumentView.as_view(), 
        name='class_document_upload'),
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
    # return a list of incidents
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
