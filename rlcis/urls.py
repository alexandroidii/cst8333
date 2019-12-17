from django.contrib import admin
from django.urls import include, path, reverse

from . import views

app_name = 'rlcis'
urlpatterns = [
    path(
        '',
        views.index,
        name='home'),
    # path(
    #     'admin/'
    #     admin.site.urls,
    #     name='admin'),
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
        'search/',
        views.incident_search,
        name='incident_search'),
]
