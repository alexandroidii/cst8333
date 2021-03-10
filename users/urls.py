from django.urls import (include, path, reverse,)
from . import views
from .views import  VerificationView,RequestPasswordResetEmail,CompletePasswordReset ,LoginView
from users import views as user_views
from django.contrib.auth import views as auth_views


app_name = 'users'
urlpatterns = [

 path('', user_views.index, name='home'),
 path('register/', user_views.register, name='register'),
 #path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'), #default Django
 path('login/', user_views.LoginView.as_view(), name='login'),
 path('logout/', user_views.LogoutView.as_view(), name='logout'),
 path('activate_account/<uidb64>/<token>', VerificationView.as_view(), name='activate_account'),
 path('password_reset/', RequestPasswordResetEmail.as_view(), name="password_reset"),
 path('profile/', user_views.profile, name='profile'),
 path('set-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name='set-new-password'),
]