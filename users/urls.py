from django.urls import (include, path, reverse,)
from . import views
from .views import  VerificationView,RequestPasswordResetEmail,CompletePasswordReset ,LoginView
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


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
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
                          
