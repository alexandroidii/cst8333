from django.contrib import admin

from .models import Incident, Reviewer

# Register your models here.
admin.site.register(Incident)
admin.site.register(Reviewer)
