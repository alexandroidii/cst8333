from rlcs.tables import ReviewerScenarioTable
from django.contrib import admin
from django.urls import (
    include, path, reverse,
)
from django.conf import settings
from django.conf.urls.static import static
from .views import FilteredScenarioListView

from . import views

""" 
CCS Urls to direct navigation through the app - all application views 
are imported.

App Namespace: 'rlcs' even though the app is now renamed to CCS.

Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19
"""


app_name = 'rlcs'
urlpatterns = [

    # root path for the home page
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('add_scenario/', views.scenario_form, name="scenario_insert"),
    path('delete_document/', views.deleteDocument, name='delete_document'),
    path('scenarios/<int:id>/', views.scenario_form, name='scenario_update'),
    path('save_scenario/', views.save_scenario, name='save_scenario'),
    path('delete_scenario/<int:id>/', views.scenario_delete, name='scenario_delete'),
    # return a list of Scenarios
    path('scenarios/', FilteredScenarioListView.as_view(), name='scenarios'),
    path('publish/<int:id>', views.publish_scenario, name='publish'),
] + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

