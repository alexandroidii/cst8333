
from django.contrib import admin
from django.urls import include, path
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('users.urls')),
    path('rlcis/', include('rlcis.urls',namespace='rlcis')),
    path('admin/', admin.site.urls),    
]
