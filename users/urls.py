from django.urls import (include, path, reverse,)
from . import views
from .views import  VerificationView,RequestPasswordResetEmail,CompletePasswordReset ,LoginView
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

"""
Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19

CCS Views that are directed via url mappings handled herein.
As there are two Djano applications (rlcs and users) within the project, a url mapping is specific to each.
Upon access to the complete application via an http request i.e http://127.0.0.1:8000 , the users app is the primary directive into the 
application.Specfic url mappings are contained for users authentication related functions including registration, authentication, profile etc.
However, the landing page and MEDIA_URL mapping do get re-directed to the rlcs app for specific 'CCS Case' related functionaly.

"""

app_name = 'users'
urlpatterns = [
    path('', user_views.landing, name='landing'),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.LoginView.as_view(), name='login'),
    path('logout/', user_views.LogoutView.as_view(), name='logout'),
    path('activate_account/<uidb64>/<token>', VerificationView.as_view(), name='activate_account'),
    path('password_reset/', RequestPasswordResetEmail.as_view(), name="password_reset"),
    path('profile/', user_views.profile, name='profile'),
    path('set-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name='set-new-password'),
] + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
