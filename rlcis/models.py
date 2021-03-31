import datetime
import os

from django.db import models
from django.db.models import Model
from django.forms import ModelForm
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser


class BribeType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BribedBy(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BribeInitiator(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BribeFacilitator(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BribeRecipient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class IndustryType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class LevelOfAuthority(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

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

class Reviewer(Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    employee_id = models.IntegerField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

"""
Class Scenario: Attributes describing the scenario model.

The reviewer will be used to review the scenarios.

"""
class Scenario(Model):
    # #Bribe Types
    # CASH = 'CA'
    # FAVORS = 'FA'
    # GRATUITY = 'GR'
    # GIFTS = 'GI'

    # #Bribed By Types
    # AGENT = 'AG'
    # THIRD_PARTY = 'TP'
    # PUBLIC_OFFICIAL = 'PO'

    # #Industry Types
    # ADVERTISING = 'AD'
    # AGRICULTURE = 'AG'
    # CONSTRUCTION = 'CN'
    # COMMUNICATIONS = 'CM'
    # EDUCATION = 'ED'
    # ENTERTAINMENT = 'EN'
    # FASION = 'FA'
    # FINANCE = 'FI'
    # INFORMATION_TECHNOLOGY = 'IT'
    # MANUFACTURING = 'MA'
    # RETAIL = 'RE'
    # TECHNOLOGY = 'TE'
    # TRANSPORTATION = 'TR'

    # # Levels
    # LOCAL = 'LO'
    # STATE = 'ST'
    # NATIONAL = 'NA'

    # General types related to all options
    # 
    # List of dictionaries used to relate to database attribute values used
    # in drop-down fields in BRIBE_TYPE, BRIBED_BY and INDUSTRY_TYPE drop downs
    # scenario and scenario forms

    # OTHER = 'OT'

    # BRIBE_TYPE_CHOICES = [
    #     (CASH, 'Cash'),
    #     (FAVORS, 'Favors'),
    #     (GRATUITY, 'Gratuity'),
    #     (GIFTS, 'Gifts'),
    #     (OTHER, 'Other Bribe Type'),
    # ]
    # BRIBED_BY_CHOICES = [
    #     (AGENT, 'Agent'),
    #     (THIRD_PARTY, 'Third Party'),
    #     (PUBLIC_OFFICIAL, 'Public Official'),
    #     (OTHER, 'Bribed by Other'),
    # ]
    # INDUSTRY_TYPE_CHOICES = [
    #     (ADVERTISING, 'Advertising'),
    #     (AGRICULTURE, 'Agriculture'),
    #     (CONSTRUCTION, 'Construction'),
    #     (COMMUNICATIONS, 'Communications'),
    #     (EDUCATION, 'Education'),
    #     (ENTERTAINMENT, 'Entertainment'),
    #     (FASION, 'Fashion'),
    #     (FINANCE, 'Finance'),
    #     (INFORMATION_TECHNOLOGY, 'Information Technology'),
    #     (MANUFACTURING, 'Manufacturing'),
    #     (RETAIL, 'Retail'),
    #     (TECHNOLOGY, 'Technology'),
    #     (TRANSPORTATION, 'Transportation'),
    #     (OTHER, 'Other Transportation Type'),

    # ]

    # LEVEL_CHOICES = [
    #     (LOCAL, 'Local'),
    #     (STATE, 'State/Provincial'),
    #     (NATIONAL, 'National'),
    # ]

    # company_name attribute in scenario table as defined
    company_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
     # scenario_summary attribute in scenario table as defined
    scenario_summary = models.CharField(
        max_length=200,
        null=True,
    )
    # scenario_details attribute in scenario table as defined
    scenario_details = models.TextField(
        null=True,
    )

    #Describes the risks reported in the scenario
    risks = models.TextField(
        null=True,
    )

    # how was the scenario resolved?
    resolution = models.TextField(
        null=True,
    )

    # country attribute in scenario table as defined
    country = models.CharField(
        max_length=60,
        null=True,
        blank=True,
)
    # region attribute in scenario table as defined
    region = models.CharField(
        max_length=60,
        null=True,
        blank=True,
    )
    # location attribute in scenario table as defined
    location = models.CharField(
        max_length=60,
        null=True,
        blank=True,
    )
    
    # bribe_initiator attribute in incident table as defined
    bribe_initiator = models.ForeignKey(
        BribeInitiator,
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
        BribeFacilitator,
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
        BribeRecipient,
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
        BribedBy,
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
        BribeType,
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
        IndustryType,
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
        LevelOfAuthority,
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
        Reviewer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    # This will be used to determine if a scenario has been reviewed and can be public
    is_reviewed = models.BooleanField(null=True,default=False,help_text="Has this been reviewed?",)

    # resolution_date attribute in scenario table as defined
    reviewed_date = models.DateField(null=True,blank=True,)

    # submitter of the scenario
    submitter = models.ForeignKey(Reviewer,on_delete=models.CASCADE,null=True,blank=True,)

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
    email = models.EmailField(
        null=True,
        blank=True,
    )


    # Return string repesenation of pk and scenario summary (used in t/s)
    def __str__(self):
        return str(self.pk) 
        # + " " + self.scenario_summary 

    def get_absolute_url(self):
        return reverse('scenario_update', kwargs={'pk': self.pk})

class ScenarioDocument(models.Model):
    scenario = models.ForeignKey(Scenario, default=None, on_delete=models.CASCADE)
 
    document = models.FileField(upload_to='scenarios/uploads/')
    
    def __str__(self):
        return self.scenario.scenario_summary

    def filename(self):
        return os.path.basename(self.document.name)
