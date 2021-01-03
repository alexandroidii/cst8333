"""cst8333 URL Configuration

The project Url file maps navigation through the defined apps.
Employs routing for both default application (admin/) and
rlcis application. (rlcis/) will direct all requests starting
from rlcis/ to the application urls file within the application (rlcis app folder)


Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19

"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = [
    path('', include('rlcis.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
