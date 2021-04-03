from django.contrib import admin

from .models import  Scenario, Reviewer, ScenarioDocument
from .models_dropdown import BribeFacilitator, BribeInitiator, BribeRecipient, BribeType, BribedBy,IndustryType, LevelOfAuthority
""" 
RLCIS admin.py - used to display models for admin pannel.

Models Scenario, Reviewer defined as input.

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

# admin.site.register(Scenario)
admin.site.register(Reviewer)
admin.site.register(BribeType)
admin.site.register(BribeInitiator)
admin.site.register(BribeFacilitator)
admin.site.register(BribeRecipient)
admin.site.register(IndustryType)
admin.site.register(LevelOfAuthority)
admin.site.site_url= "/"

class ScenarioDocumentAdmin(admin.StackedInline):
    model = ScenarioDocument

@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    inlines = [ScenarioDocumentAdmin]

    class Meta:
        model = Scenario

@admin.register(ScenarioDocument)
class ScenarioDocumentAdmin(admin.ModelAdmin):
    pass