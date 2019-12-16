from django.contrib import admin

from .models import Incident, Reviewer

# Register your models here.
admin.site.site_header = "RLCIS Admin"
admin.site.site_title = "RLCIS Admin Area"
admin.site.index_title = "Welcome to the RLCIS Admin area"

admin.site.register(Incident)
admin.site.register(Reviewer)