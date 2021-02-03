from django.contrib import admin

from .models import Incident, Reviewer, IncidentDocument

""" 
RLCIS admin.py - used to display models for admin pannel.

Models Incident, Reviewer defined as input.

Customizations include:
site_header
site_title
index_title.

Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19
"""

admin.site.site_header = "RLCIS Admin"
admin.site.site_title = "RLCIS Admin Area"
admin.site.index_title = "Welcome to the RLCIS Admin area"

# admin.site.register(Incident)
admin.site.register(Reviewer)
admin.site.site_url= "/"

class IncidentDocumentAdmin(admin.StackedInline):
    model = IncidentDocument

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    inlines = [IncidentDocumentAdmin]

    class Meta:
        model = Incident

@admin.register(IncidentDocument)
class IncidentDocumentAdmin(admin.ModelAdmin):
    pass