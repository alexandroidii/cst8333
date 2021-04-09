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
    path('add_scenario/', views.scenario_form, name="scenario_insert"),
    path('delete_document/', views.deleteDocument, name='delete_document'),
    path('scenarios/<int:id>/', views.scenario_form, name='scenario_update'),
    path('save_scenario/', views.save_scenario, name='save_scenario'),
    path('delete_scenario/<int:id>/', views.scenario_delete, name='scenario_delete'),
    # return a list of Scenarios
    path('scenarios/', views.scenarios, name='scenarios'),
    path('publish/', views.publish_scenario, name='publish'),
    path(r'^scenarios_table$', views.ScenariosTableView, name='scenarios_table'),

   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
