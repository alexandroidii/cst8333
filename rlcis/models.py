import datetime
import os
import rlcis.models_dropdown as dropDowns

from django.contrib.auth.forms import UserModel
import users.models as Users

from django.db import models
from django.db.models import Model
from django.forms import ModelForm
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.apps import apps



# class BribeType(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class BribedBy(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class BribeInitiator(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class BribeFacilitator(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class BribeRecipient(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class IndustryType(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class LevelOfAuthority(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name



""" 
RLCIS models.py define the structure to the underlying database.
Using python manage.py makemigrations followed by python manage.py migrate
defines the noted attributes below for the application within the specified database. 
It uses the settings.py file DATABASES dicitonary for database schema/credential/connection 

App Namespace: 'rlcis'

Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19



Class Reviewer: Attributes describing the Reviewer model.

The reviewer will be used to review the scenarios.

"""

class Reviewer(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    employee_id = models.IntegerField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

"""
Class Scenario: Attributes describing the scenario model.

The reviewer will be used to review the scenarios.

"""

class Scenario(models.Model):

    # company_name attribute in incident table as defined
    company_name = models.CharField(max_length=100, null=True, blank=True)

     # incident_summary attribute in incident table as defined
    scenario_summary = models.CharField(max_length=200, null=True)
    
    # incident_details attribute in incident table as defined
    scenario_details = models.TextField(null=True)

    #Describes the risks reported in the incident
    risks = models.TextField(null=True)

    # how was the incident resolved?
    resolution = models.TextField(null=True)

    # country attribute in incident table as defined
    country = models.CharField(max_length=60, null=True, blank=True)

    # region attribute in incident table as defined
    region = models.CharField(max_length=60, null=True, blank=True)

    # location attribute in incident table as defined
    location = models.CharField(max_length=60, null=True, blank=True)

    # # bribed_by attribute in incident table as defined
    # bribed_by = models.ForeignKey(BribedBy, models.SET_NULL, blank=True, null=True)
    # bribe_initiator attribute in incident table as defined
    bribe_initiator = models.ForeignKey(
        dropDowns.BribeInitiator,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    # bribe_initiator_other attribute in scenario table as defined
    bribe_initiator_other = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    # bribe_facilitator attribute in incident table as defined
    bribe_facilitator = models.ForeignKey(
        dropDowns.BribeFacilitator,
        models.SET_NULL,
        blank=True,
        null=True,
    )
    
    # bribe_facilitator_other attribute in scenario table as defined
    bribe_facilitator_other = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    # bribe_recipient attribute in incident table as defined
    bribe_recipient = models.ForeignKey(
        dropDowns.BribeRecipient,
        models.SET_NULL,
        blank=True,
        null=True,
    )
    
    # bribe_recipient_other attribute in scenario table as defined
    bribe_recipient_other = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    
    # bribed_by attribute in incident table as defined

    bribed_by = models.ForeignKey(
        dropDowns.BribedBy,
        models.SET_NULL,
        blank=True,
        null=True,
    )
    
    
    # bribed_by = models.CharField(
    #     max_length=2,
    #     choices=BRIBED_BY_CHOICES,
    #     default=OTHER,
    # )
    # # bribed_by_other attribute in scenario table as defined
    # bribed_by_other = models.CharField(
    #     max_length=100,
    #     null=True,
    #     blank=True,
    # )
    # bribed_type attribute in scenario table as defined
    bribe_type = models.ForeignKey(
        dropDowns.BribeType,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    # bribed_type_other attribute in scenario table as defined
    bribe_type_other = models.CharField(
        max_length=60,
        null=True,
        blank=True,
    )
    
    # bribe_type = models.CharField(
    #     max_length=2,
    #     choices=BRIBE_TYPE_CHOICES,
    #     default=OTHER,
    # )
    # industry_type attribute in scenario table as defined
    industry_type = models.ForeignKey(
        dropDowns.IndustryType,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    # industry_type_other attribute in scenario table as defined
    industry_type_other = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    # levelOfAuthority attribute in scenario table as defined
    levelOfAuthority = models.ForeignKey(
        dropDowns.LevelOfAuthority,
        models.SET_NULL,
        blank=True,
        null=True,
    )
    
    # level = models.CharField(
    #     max_length=2,
    #     choices=LEVEL_CHOICES,
    #     null=True,
    #     blank=True,
    #     # default=OTHER,
    # )
    # first_occurence attribute in scenario table as defined
    first_occurence = models.DateField(
        null=True,
        blank=True,
    )
    # resolution_date attribute in scenario table as defined
    resolution_date = models.DateField(
        null=True,
        blank=True,
    )
    # reviewer attribute in scenario table as defined
    reviewer = models.ForeignKey(
        Users.Users,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reviewer"
    )

    # This will be used to determine if a scenario has been reviewed and can be public
    is_reviewed = models.BooleanField(null=True,default=False,help_text="Has this been reviewed?",)

    # resolution_date attribute in scenario table as defined
    reviewed_date = models.DateField(null=True,blank=True,)

    # submitter of the scenario
    submitter = models.ForeignKey(Users.Users,on_delete=models.CASCADE,null=True,blank=True,related_name="submitter")

    # resolution_date attribute in scenario table as defined
    submitted_date = models.DateField(null=True,blank=True,)

    # anonymous attribute in scenario table as defined
    anonymous = models.BooleanField(
        null=True,
        default=False,
        help_text="Would you like to submit this scenario Anonymously?",
    )
    # scenario attribute in scenario table as defined
    is_training_scenario = models.BooleanField(
        default=False,
        help_text="Is this a real life Scenario or a Ficticous Scenario?",
    )

    #public email address that can be contacted
    email = models.EmailField(null=True, blank=True)


    # Return string repesenation of pk and scenario summary (used in t/s)
    def __str__(self):
        return str(self.pk) 
        # + " " + self.scenario_summary 

    # def create_incident(sender, instance,**kwargs):
    #     instance.incident.save()
    #     print('Incident saved!')

    # post_save.connect(create_incident, sender=Incident)

    def get_absolute_url(self):
        return reverse('scenario_update', kwargs={'pk': self.pk})

class ScenarioDocument(models.Model):
    scenario = models.ForeignKey(Scenario, default=None, on_delete=models.CASCADE)
 
    document = models.FileField(upload_to='scenarios/uploads/')
    
    def __str__(self):
        return self.scenario.scenario_summary

    def filename(self):
        return os.path.basename(self.document.name)
