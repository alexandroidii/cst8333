import collections
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Row, Column, HTML
from crispy_forms.bootstrap import Accordion, AccordionGroup
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.utils import formats

from .models import BribedBy, Scenario, ScenarioDocument



""" 
RLCIS forms used when populating the template fields.  

Functions:
DateInput -- Used to set the input type of a field to 'date'
SearchForm -- form used for the search function of both Scenarios and Scenarios
ScenarioForm -- form used for both scenarios and scenarios when populating templates

Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19
"""


class DateInput(forms.DateInput):
    input_type = 'date'

"""
The Search Form uses the 'q' field to take in a users query
which is used to search through the scenario objects.  
Both Scenarios and Scenarios go through this search
    
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
The Scenario form is used to populate the templates for CrUD operations
on the Scenario Object.  Both Scenarios and Scenarios use this form.  
The different is when the 'scenario' Boolean is set to true, then 
then object is considered to be a Scenario instead of an Scenario.
    
Fields:

anonymous           -- Boolean field to set the submission as anonymous.  This 
                        disables the country, region, location and company name fields
company_name        -- Optional field 
scenario_summary    -- Required
scenario_details    -- Required
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
is_training_scenario-- Optional.  This determines if the Scenario is actually a Scenario or a training version
industry_type       -- Required
industry_type_other -- Optional field only if industry_type is set to Other
level               -- Optional field
email               -- Optional field for publicly displayed email for a scenario
"""
class ScenarioForm(forms.ModelForm):
    anonymous = forms.BooleanField(
        required=False, 
        label="Submit Anonymously?",
        widget=forms.CheckboxInput(attrs={'class': 'anonymousToggle'})
    )

    # file = forms.FileField(
    #     required=False, 
    #     label="Supporting Documents",
    #     widget=forms.FileInput(attrs={'multiple':'true'})
    # )

    class Meta:
        model = Scenario
        fields = [
            'company_name',
            'anonymous',
            'scenario_summary',
            'scenario_details',
            'country',
            'region',
            'location',
            'bribed_by',
            # 'bribed_by_other',
            'bribe_type',
            # 'bribe_type_other',
            'first_occurence',
            'resolution_date',
            'reviewer',
            'is_training_scenario',
            'industry_type',
            # 'industry_type_other',
            'levelOfAuthority',
            'email',
            'risks',
            'resolution'
        ]
        labels = { # assign all the labels for the fields used in the template automatically
            'company_name': 'Company Name',
            'scenario_summary': 'Scenario Summary',
            'scenario_details': 'Scenario Details',
            'country': 'Country',
            'region': 'Region',
            'bribed_by': 'Bribed By',
            # 'bribed_by_other': 'Bribed By Other',
            'bribe_type': 'Bribe Type',
            # 'bribe_type_other': 'Bribe Type Other',
            'first_occurence': 'First Occurence',
            'location': 'Location',
            'resolution_date': 'Resolution Date',
            'reviewer': 'Reviewer',
            'industry_type': 'Industry Type',
            # 'industry_type_other': 'Industry Type Other',
            'levelOfAuthority':'Level of Authority of Public Official',
            'email':'Public Email',
            'risks':'What where the risks of this scenario?',
            'resolution':'How was the scenario resolved?'
        }
        widgets = {
            'first_occurence': DateInput(), # set the first_occurent input_type to 'date'
            'resolution_date': DateInput(), # set the resolution_date input_type to 'date'
            'scenario_details': forms.Textarea(attrs={'rows':2}), # sets the number of rows in the scenario_details to 2
            'risks': forms.Textarea(attrs={'rows':2}), # sets the number of rows in the scenario_details to 2
            'resolution': forms.Textarea(attrs={'rows':2}), # sets the number of rows in the scenario_details to 2
            # 'bribed_by': ChoiceTextField(queryset=BribedBy.objects.all()),
            # 'bribe_type': ChoiceTextField(queryset=BribedBy.objects.all()),
            # 'industry_type': ChoiceTextField(queryset=BribedBy.objects.all()),
            # 'levelOfAuthority': ChoiceTextField(queryset=BribedBy.objects.all()),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'scenarioForm'
        self.helper.layout = Layout(
            Row(
                Column('anonymous', css_class='form-group col-sm-2 col-md-6'),
                Column('email', css_class='form-group col-sm-4 col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('country', css_class='form-group col-sm-2 col-md-4'),
                Column('region', css_class='form-group col-sm-2 col-md-4'),
                Column('location', css_class='form-group col-sm-2 col-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('company_name', css_class='form-group col-sm-2 col-md-4 anonymous'),
                Column('industry_type', css_class='form-group col-sm-2 col-md-4'),
                Column('levelOfAuthority', css_class='form-group col-sm-2 col-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('scenario_summary', css_class='form-group col-sm-4 col-md-12'),
                css_class='form-row'
            ),
            Row(
                Column('bribed_by', css_class='form-group col-sm-4 col-md-6'),
                Column('bribe_type', css_class='form-group col-sm-4 col-md-6'),
                css_class='form-row'
            ),
            # Row(
            #     Column('bribed_by_other', css_class='form-group col-sm-4 col-md-6'),
            #     Column('bribe_type_other', css_class='form-group col-sm-4 col-md-6'),
            #     css_class='form-row'
            # ),
            Row(
                Column('scenario_details', css_class='form-group col-sm-4 col-md-12'),
                css_class='form-row'
            ),
            Row(
                Column('risks', css_class='form-group col-sm-4 col-md-12'),
                css_class='form-row'
            ),
            Row(
                Column('resolution', css_class='form-group col-sm-4 col-md-12'),
                css_class='form-row'
            ),
            Row(
                Column('first_occurence', css_class='form-group col-sm-4 col-md-6'),
                Column('resolution_date', css_class='form-group col-sm-4 col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column(HTML('<input type="file" multiple>'),css_class='col-sm-12 col-md-12'),
                css_class='form-row'
            ),
            Row(
                Column(
                    Accordion(
                        AccordionGroup('Supporting Documents',
                            HTML(
                                '{% for f in files %}'
                                + '<div class="card card-body d-block" id="file-{{ f.pk }}">'
                                + '<button class="btn deleteFileBtn" type="button" data-docid="{{ f.pk }}" data-filename="{{ f.filename }}">'
                                + '<i class="fas fa-trash-alt"></i>'
                                + '</button>'
                                + '<a href="{{f.document.url}}" target="_blank">{{ f.filename }}</a>'
                                + '</div>'
                                + '{% endfor %}"'
                            )    
                        )
                    )
                )
            )
        )
        # set which fields are not required.
        # self.fields['bribed_by_other'].required = False
        # self.fields['bribe_type_other'].required = False
        # self.fields['industry_type_other'].required = False
        # self.fields['level'].required = False
        self.fields['company_name'].required = False
        self.fields['anonymous'].required = False
        self.fields['first_occurence'].required = False
        self.fields['resolution_date'].required = False
        self.fields['reviewer'].required = False
        self.fields['email'].required = False
        # self.fields['level'].required = False
        self.fields['risks'].required = False
        self.fields['resolution'].required = False

class ScenarioDocumentForm(forms.ModelForm):
    
    class Meta:
        model = ScenarioDocument
        fields = [
            'scenario',
            'document',
        ]

# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email','password1', 'password2']

class ListTextWidget(forms.Select):
    template_name = 'listtxt.html'

    def format_value(self, value):
        if value == '' or value is None:
            return ''
        if self.is_localized:
            return formats.localize_input(value)
            return str(value)

class ChoiceTextField(forms.ModelChoiceField):
    widget=ListTextWidget()      