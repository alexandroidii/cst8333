import collections
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Row, Column
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import Incident, Document, IncidentDocument

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name','files','images')
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple':True}),
        }


    

""" 
RLCIS forms used when populating the template fields.  

Functions:
DateInput -- Used to set the input type of a field to 'date'
SearchForm -- form used for the search function of both Incidents and Scenarios
IncidentForm -- form used for both incidents and scenarios when populating templates

Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19
"""


class DateInput(forms.DateInput):
    input_type = 'date'

"""
The Search Form uses the 'q' field to take in a users query
which is used to search through the incident objects.  
Both Incidents and Scenarios go through this search
    
Fields:

q -- CharField used to store the users query
"""
class SearchForm(forms.Form):
    q = forms.CharField(
        label = 'Search',
        max_length = 200,
        help_text="Search on any of the text fields below." ,
        )
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        helper.form_show_labels = False #removes the label for the query field when it is initialized

"""
The Incident form is used to populate the templates for CrUD operations
on the Incident Object.  Both Incidents and Scenarios use this form.  
The different is when the 'scenario' Boolean is set to true, then 
then object is considered to be a Scenario instead of an Incident.
    
Fields:

anonymous           -- Boolean field to set the submission as anonymous.  This 
                        disables the country, region, location and company name fields
company_name        -- Optional field 
incident_summary    -- Required
incident_details    -- Required
country             -- Optional
region              -- Optional
location            -- Optional
bribed_by           -- Required 
bribed_by_other     -- Optional field only if bribed_by is set to Other
bribe_type          -- Required
bribe_type_other    -- Optional field only if bribe_type is set to Other
first_occurence     -- Optional
resolution_date     -- Optional
reviewer            -- Optional
scenario            -- Required but hidden.  This determines if the Incident is actually a Scenario
industry_type       -- Required
industry_type_other -- Optional field only if industry_type is set to Other
level               -- Optional field
"""
class IncidentForm(forms.ModelForm):
    anonymous = forms.BooleanField(
        required=False, 
        label="Submit Anonymously?",
        widget=forms.CheckboxInput(attrs={'class': 'anonymousToggle'})
    )

    class Meta:
        model = Incident
        fields = [
            'company_name',
            'anonymous',
            'incident_summary',
            'incident_details',
            'country',
            'region',
            'location',
            'bribed_by',
            'bribed_by_other',
            'bribe_type',
            'bribe_type_other',
            'first_occurence',
            'resolution_date',
            'reviewer',
            'scenario',
            'industry_type',
            'industry_type_other',
            'level',
            'email',
            # 'documents',

        ]
        labels = { # assign all the labels for the fields used in the template automatically
            'company_name': 'Company Name',
            'incident_summary': 'Incident Summary',
            'incident_details': 'Incident Details',
            'country': 'Country',
            'region': 'Region',
            'bribed_by': 'Bribed By',
            'bribed_by_other': 'Bribed By Other',
            'bribe_type': 'Bribe Type',
            'bribe_type_other': 'Bribe Type Other',
            'first_occurence': 'First Occurence',
            'location': 'Location',
            'resolution_date': 'Resolution Date',
            'reviewer': 'Reviewer',
            'industry_type': 'Industry Type',
            'industry_type_other': 'Industry Type Other',
            'level':'Level',
            'email':'Public Email',
        }
        widgets = {
            'first_occurence': DateInput(), # set the first_occurent input_type to 'date'
            'resolution_date': DateInput(), # set the resolution_date input_type to 'date'
            'incident_details': forms.Textarea(attrs={'rows':2}), # sets the number of rows in the incident_details to 2
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'incidentForm'
        self.helper.layout = Layout(
            Row(
                Column('anonymous', css_class='form-group col-sm-2 col-md-6'),
                Column('email', css_class='form-group col-sm-4 col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('company_name', css_class='form-group col-sm-2 col-md-4 anonymous'),
                Column('industry_type', css_class='form-group col-sm-2 col-md-4'),
                Column('level', css_class='form-group col-sm-2 col-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('incident_summary', css_class='form-group col-sm-4 col-md-12'),
                css_class='form-row'
            ),
            Row(
                Column('incident_details', css_class='form-group col-sm-4 col-md-12'),
                css_class='form-row'
            ),
            Row(
                Column('bribed_by', css_class='form-group col-sm-4 col-md-6'),
                Column('bribe_type', css_class='form-group col-sm-4 col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('bribed_by_other', css_class='form-group col-sm-4 col-md-6'),
                Column('bribe_type_other', css_class='form-group col-sm-4 col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('first_occurence', css_class='form-group col-sm-4 col-md-6'),
                Column('resolution_date', css_class='form-group col-sm-4 col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('country', css_class='form-group col-sm-2 col-md-4'),
                Column('region', css_class='form-group col-sm-2 col-md-4'),
                Column('location', css_class='form-group col-sm-2 col-md-4'),
                css_class='form-row'
            )
        )
        # set which fields are not required.
        self.fields['bribed_by_other'].required = False
        self.fields['bribe_type_other'].required = False
        self.fields['industry_type_other'].required = False
        self.fields['level'].required = False
        self.fields['company_name'].required = False
        self.fields['anonymous'].required = False
        self.fields['first_occurence'].required = False
        self.fields['resolution_date'].required = False
        self.fields['reviewer'].required = False
        self.fields['email'].required = False

class IncidentDocumentForm(forms.ModelForm):
    
    class Meta:
        model = IncidentDocument
        fields = [
            'incident',
            'document',
        ]

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']

      