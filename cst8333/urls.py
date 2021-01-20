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
from django.contrib.auth import views as auth_views
from django.urls import include, path
from users import views as user_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('rlcis.urls')),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_view.profile, name='profile'),
    path('register/', user_view.register, name='register'),

]
#urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
