import datetime
import os

from django.db import models
from django.db.models import Model
from django.forms import ModelForm
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser


class Document(models.Model):
    name = models.CharField(max_length=100)
    files = models.FileField(upload_to='incidents/uploads/')
    images = models.ImageField(upload_to='incidents/images/', null=True, blank=True)

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

The reviewer will be used to review the incidents.

"""

class Reviewer(Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    employee_id = models.IntegerField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

"""
Class Incident: Attributes describing the incident model.

The reviewer will be used to review the incidents.

"""
class Incident(Model):
    #Bribe Types
    CASH = 'CA'
    FAVORS = 'FA'
    GRATUITY = 'GR'
    GIFTS = 'GI'

    #Bribed By Types
    AGENT = 'AG'
    THIRD_PARTY = 'TP'
    PUBLIC_OFFICIAL = 'PO'

    #Industry Types
    ADVERTISING = 'AD'
    AGRICULTURE = 'AG'
    CONSTRUCTION = 'CN'
    COMMUNICATIONS = 'CM'
    EDUCATION = 'ED'
    ENTERTAINMENT = 'EN'
    FASION = 'FA'
    FINANCE = 'FI'
    INFORMATION_TECHNOLOGY = 'IT'
    MANUFACTURING = 'MA'
    RETAIL = 'RE'
    TECHNOLOGY = 'TE'
    TRANSPORTATION = 'TR'



    # General types related to all options
    # 
    # List of dictionaries used to relate to database attribute values used
    # in drop-down fields in BRIBE_TYPE, BRIBED_BY and INDUSTRY_TYPE drop downs
    # incident and scenario forms

    OTHER = 'OT'

    BRIBE_TYPE_CHOICES = [
        (CASH, 'Cash'),
        (FAVORS, 'Favors'),
        (GRATUITY, 'Gratuity'),
        (GIFTS, 'Gifts'),
        (OTHER, 'Other Bribe Type'),
    ]
    BRIBED_BY_CHOICES = [
        (AGENT, 'Agent'),
        (THIRD_PARTY, 'Third Party'),
        (PUBLIC_OFFICIAL, 'Public Official'),
        (OTHER, 'Bribed by Other'),
    ]
    INDUSTRY_TYPE_CHOICES = [
        (ADVERTISING, 'Advertising'),
        (AGRICULTURE, 'Agriculture'),
        (CONSTRUCTION, 'Construction'),
        (COMMUNICATIONS, 'Communications'),
        (EDUCATION, 'Education'),
        (ENTERTAINMENT, 'Entertainment'),
        (FASION, 'Fasion'),
        (FINANCE, 'Finance'),
        (INFORMATION_TECHNOLOGY, 'Information Technology'),
        (MANUFACTURING, 'Manufacturing'),
        (RETAIL, 'Retail'),
        (TECHNOLOGY, 'Technology'),
        (TRANSPORTATION, 'Transportation'),
        (OTHER, 'Other Transportation Type'),

    ]

    # company_name attribute in incident table as defined
    company_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
     # incident_summary attribute in incident table as defined
    incident_summary = models.CharField(
        max_length=200,
        null=True,
    )
    # incident_details attribute in incident table as defined
    incident_details = models.TextField(
        null=True,
    )
    # country attribute in incident table as defined
    country = models.CharField(
        max_length=60,
        null=True,
        blank=True,
)
    # region attribute in incident table as defined
    region = models.CharField(
        max_length=60,
        null=True,
        blank=True,
    )
    # location attribute in incident table as defined
    location = models.CharField(
        max_length=60,
        null=True,
        blank=True,
    )
    # bribed_by attribute in incident table as defined
    bribed_by = models.CharField(
        max_length=2,
        choices=BRIBED_BY_CHOICES,
        default=OTHER,
    )
    # bribed_by_other attribute in incident table as defined
    bribed_by_other = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    # bribed_type attribute in incident table as defined
    bribe_type = models.CharField(
        max_length=2,
        choices=BRIBE_TYPE_CHOICES,
        default=OTHER,
    )
    # bribed_type_other attribute in incident table as defined
    bribe_type_other = models.CharField(
        max_length=60,
        null=True,
        blank=True,
    )
    # industry_type attribute in incident table as defined
    industry_type = models.CharField(
        max_length=2,
        choices=INDUSTRY_TYPE_CHOICES,
        default=OTHER,
    )
    # industry_type_other attribute in incident table as defined
    industry_type_other = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    # first_occurence attribute in incident table as defined
    first_occurence = models.DateField(
        null=True,
        blank=True,
    )
    # resolution_date attribute in incident table as defined
    resolution_date = models.DateField(
        null=True,
        blank=True,
    )
    # reviewer attribute in incident table as defined
    reviewer = models.ForeignKey(
        Reviewer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    # anonymous attribute in incident table as defined
    anonymous = models.BooleanField(
        null=True,
        default=False,
        help_text="Would you like to submit this incident Anonymously?",
    )
    # scenario attribute in incident table as defined
    scenario = models.BooleanField(
        default=False,
        help_text="Is this a real life Incident or a Ficticous Scenario?",
    )

    # documents = models.FileField(blank=True)

    # document = models.ForeignKey(
    #     Document,
    #     on_delete = models.CASCADE,
    #     null=True,
    #     blank=True,
    # )
    # Return string repesenation of pk and incident summary (used in t/s)
    def __str__(self):
        return str(self.pk) 
        # + " " + self.incident_summary 

    def get_absolute_url(self):
        return reverse('incident_update', kwargs={'pk': self.pk})

class IncidentDocument(models.Model):
    incident = models.ForeignKey(Incident, default=None, on_delete=models.CASCADE)
    document = models.FileField(upload_to='incidents/uploads/')
    
    def __str__(self):
        return self.incident.incident_summary

    def filename(self):
        return os.path.basename(self.document.name)






"""
class NewContributer(AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True)
    user_name models.CharField(max_length=150, unique=True)
    """
