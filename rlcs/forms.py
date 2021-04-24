import collections
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Row, Column, HTML, Submit, Reset
from crispy_forms.bootstrap import Accordion, AccordionGroup
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from django.utils import formats
from .models import Scenario, ScenarioDocument
from .models_dropdown import BribedBy



""" 
CCS forms used when populating the template fields.  

Functions:
DateInput -- Used to set the input type of a field to 'date'
SearchForm -- form used for the search function of both Scenarios and Scenarios
ScenarioForm -- form used for both scenarios and scenarios when populating templates

Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19
"""


class ReviewerScenarioFilterForm(forms.Form):
    model = Scenario
    fields = [
                'country',
                'region',
                'location',
                'company_name',
                'industry_type',
                'levelOfAuthority',
                'bribe_initiator',
                'bribe_facilitator',
                'bribe_recipient',
                'bribe_type',
                'scenario_summary',
                'scenario_details',
                'reviewer',
                'email',
                'submitted_date',
                'is_reviewed',
            ]
    
    def __init__(self, *args, **kwargs):
        super(ReviewerScenarioFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.layout = Layout(
            Accordion(
                AccordionGroup('Search Criteria',
                    Row(
                        Column("bribe_initiator", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("bribe_facilitator", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("bribe_recipient", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("bribe_type", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("scenario_summary", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("scenario_details", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        css_class='form-row'
                        ),
                    Row(
                        Column("country", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("region",css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("location",css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("company_name", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("industry_type", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("levelOfAuthority", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        css_class='form-row'
                        ),
                    Row(
                        Column("submitted_date", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("email",css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("reviewer",css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("is_reviewed",css_class='col-sm-2 col-md-2', autocomplete="off"),
                        css_class='form-row'
                        ),
                    Row(
                        Column(
                            Submit('submit', 'Filter', css_class='btn btn-primary'),
                            Reset('reset filter', 'Reset Filter', css_class='btn btn-info'),
                            ), 
                        css_class='form-row'
                        ),
                        active=False,
                    ),
                ),
            )
class SubmitterScenarioFilterForm(forms.Form):
    model = Scenario
    fields = [
                'country',
                'region',
                'location',
                'company_name',
                'industry_type',
                'levelOfAuthority',
                'bribe_initiator',
                'bribe_facilitator',
                'bribe_recipient',
                'bribe_type',
                'scenario_summary',
                'scenario_details',
            ]
    
    def __init__(self, *args, **kwargs):
        super(SubmitterScenarioFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.layout = Layout(
            Accordion(
                AccordionGroup('Search Criteria',
                    Row(
                        Column("bribe_initiator", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("bribe_facilitator", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("bribe_recipient", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("bribe_type", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("scenario_summary", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("scenario_details", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        css_class='form-row'
                        ),
                    Row(
                        Column("country", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("region",css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("location",css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("company_name", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("industry_type", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column("levelOfAuthority", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        css_class='form-row'
                        ),
                    Row(
                        # Column("submitted_date", css_class='col-sm-2 col-md-2', autocomplete="off"),
                        # Column("reviewer",css_class='col-sm-2 col-md-2', autocomplete="off"),
                        Column(
                            Submit('submit', 'Filter', css_class='btn btn-primary'),
                            Reset('reset filter', 'Reset Filter', css_class='btn btn-info'),
                            ), 
                        css_class='form-row'
                        ),
                        active=False,
                    ),
                ),
            )



class DateInput(forms.DateInput):
    input_type = 'date'

def BaseScenarioFields():
    fields=[
            'company_name',
            'anonymous',
            'scenario_summary',
            'scenario_details',
            'country',
            'region',
            'location',
            'bribe_initiator',
            'bribe_facilitator',
            'bribe_recipient',
            'bribe_initiator_other',
            'bribe_facilitator_other',
            'bribe_recipient_other',
            'bribe_type',
            'bribe_type_other',
            'first_occurence',
            'resolution_date',
            'reviewer',
            'is_training_scenario',
            'industry_type',
            'industry_type_other',
            'levelOfAuthority',
            'email',
            'risks',
            'resolution',
            'is_reviewed',
        ]
    return fields

def PublicScenarioFields():
    fields=[
            'company_name',
            'region',
            'location',
            'email',
        ]
    return fields

def BaseScenarioLabels():
    labels = { # assign all the labels for the fields used in the template automatically
            'company_name': 'Company Name',
            'scenario_summary': 'Case Summary',
            'scenario_details': 'How did it start?',
            'country': 'Country',
            'region': 'Region',
            'bribe_initiator': 'Bribe Initiator',
            'bribe_facilitator': 'Bribe Facilitator',
            'bribe_recipient': 'Bribe Receipient',
            'bribe_initiator_other': 'Bribe Initiator Other',
            'bribe_facilitator_other': 'Bribe Facilitator Other',
            'bribe_recipient_other': 'Bribe Receipient Other',
            'bribed_by_other': 'Bribed By Other',
            'bribe_type': 'Bribe Type',
            'bribe_type_other': 'Bribe Type Other',
            'first_occurence': 'First Occurence',
            'location': 'Location',
            'resolution_date': 'Resolution Date',
            'reviewer': 'Reviewer',
            'industry_type': 'Industry Type',
            'industry_type_other': 'Industry Type Other',
            'levelOfAuthority':'Level of Authority of Public Official',
            'email':'Public Email',
            'risks':'What where the risks?',
            'resolution':'How was this resolved?',
            'anonymous':'Would you like to keep your Company Name, Region and Location, and Public Email address private?',
            'is_reviewed':"Has been reviewed",
        }
    return labels

def BaseScenarioWidgets():
    widgets = {
            'first_occurence': DateInput(), # set the first_occurent input_type to 'date'
            'resolution_date': DateInput(), # set the resolution_date input_type to 'date'
            'scenario_details': forms.Textarea(attrs={'rows':2}), # sets the number of rows in the scenario_details to 2
            'risks': forms.Textarea(attrs={'rows':2}), # sets the number of rows in the scenario_details to 2
            'resolution': forms.Textarea(attrs={'rows':2}), # sets the number of rows in the scenario_details to 2
            'anonymous': forms.CheckboxInput(attrs={'class': 'anonymousToggle'})
            # 'bribed_by': ChoiceTextField(queryset=BribedBy.objects.all()),
            # 'bribe_type': ChoiceTextField(queryset=BribedBy.objects.all()),
            # 'industry_type': ChoiceTextField(queryset=BribedBy.objects.all()),
            # 'levelOfAuthority': ChoiceTextField(queryset=BribedBy.objects.all()),
        }
    return widgets
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
class ScenarioFormReviewer(forms.ModelForm):
    
    class Meta:
        model = Scenario
        fields = BaseScenarioFields() + PublicScenarioFields() + ['reviewer']
        labels = BaseScenarioLabels()
        widgets = BaseScenarioWidgets()

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'scenarioForm'
        self.helper.layout = Layout(
            BaseScenarioLayout()
        )

class ScenarioFormSubmitter(forms.ModelForm):
    
    class Meta:
        model = Scenario
        fields = BaseScenarioFields() + PublicScenarioFields()
        labels = BaseScenarioLabels()
        widgets = BaseScenarioWidgets()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'scenarioForm'
        self.helper.layout = Layout(
            BaseScenarioLayout()
        )

class AnonymousScenarioFormSubmitter(forms.ModelForm):
    
    class Meta:
        model = Scenario
        fields = BaseScenarioFields()
        labels = BaseScenarioLabels()
        widgets = BaseScenarioWidgets()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'scenarioForm'
        self.helper.layout = Layout(
            AnonymousScenarioLayout()
        )

class ScenarioDocumentForm(forms.ModelForm):
    
    class Meta:
        model = ScenarioDocument
        fields = [
            'scenario',
            'document',
        ]


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


"""
This is a crispy forms Layout class that is used to generate both the submitter and reviewer version of the 
scenario form.  This dynamically creates Row/Col divs as well as other bootstrap style layouts like
accordion and rendering buttons.
"""
class BaseScenarioLayout(Layout):
    def __init__(self, *args, **kwargs):
        super().__init__(

            Row(
                Column(HTML('<h1>Case</h1>'),css_class='col-sm-12 col-md-12 text-center'),
            ),
            Row(
                Column(HTML('<p>Fill in the details of the corruption case as best as you can. Once submitted, it will be reviewed by CCS, who will contact you to confirm any details.  Once the case is reviewed and approved, it will be posted publicly.'),css_class='col-sm-12 col-md-12'),
                css_class='form-row'
            ),
            Row(
                Column('anonymous', css_class='form-group col-sm-8 col-md-8'),
                Column(HTML(
                            '{% if request.user.is_reviewer %}' +
                                    'Review Status:  {{ review_status }} <br/>' +
                                    'Reviewer:  {{ reviewer_name }} <br/>' +
                                    'Submitter:  {{ submitter_name }}' +
                            '{% endif %}' 
                        ), 
                    css_class='form-group col-sm-4 col-md-4 text-primary font-weight-bold'),
                css_class='form-row'
            ),
            Accordion(
                AccordionGroup('Identification',
                    Row(
                        Column('levelOfAuthority', css_class='form-group col-sm-2 col-md-6'),
                        Column('email', css_class='form-group col-sm-2 col-md-6'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('country', css_class='form-group col-sm-2 col-md-4'),
                        Column('region', css_class='form-group col-sm-2 col-md-4'),
                        Column('location', css_class='form-group col-sm-2 col-md-4'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('industry_type', css_class='form-group col-sm-2 col-md-4'),
                        Column('industry_type_other', css_class='form-group col-sm-2 col-md-4'),
                        Column('company_name', css_class='form-group col-sm-2 col-md-4'),
                        css_class='form-row'
                    ),
                )
            ),
            Accordion(
                AccordionGroup('Summary',
                    Row(
                        Column('scenario_summary', css_class='form-group col-sm-4 col-md-12'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('bribe_initiator', css_class='form-group col-sm-2 col-md-3'),
                        Column('bribe_facilitator', css_class='form-group col-sm-2 col-md-3'),
                        Column('bribe_recipient', css_class='form-group col-sm-2 col-md-3'),
                        Column('bribe_type', css_class='form-group col-sm-2 col-md-3'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('bribe_initiator_other', css_class='form-group col-sm-2 col-md-3'),
                        Column('bribe_facilitator_other', css_class='form-group col-sm-2 col-md-3'),
                        Column('bribe_recipient_other', css_class='form-group col-sm-2 col-md-3'),
                        Column('bribe_type_other', css_class='form-group col-sm-2 col-md-3'),
                        css_class='form-row'
                    ),
                )
            ),
            Accordion(
                AccordionGroup('Scenario Details',
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
                )
            ),
            Accordion(
                AccordionGroup('Supporting Documents',
                    Row(
                        Column(HTML('<input type="file" multiple>'),css_class='col-sm-12 col-md-12'),
                        css_class='form-row'
                    ),
                    Row(
                        Column(
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


class AnonymousScenarioLayout(Layout):
    def __init__(self, *args, **kwargs):
        super().__init__(

            Row(
                Column(HTML('<h1>Scenario</h1>'),css_class='col-sm-12 col-md-12 text-center'),
            ),
            Row(
                Column(HTML('<p>Fill in the details of the corruption scenario as best as you can. Once submitted, it will be reviewed by CCS, who will contact you to confirm any details.  Once the scenario is reviewed and approved, it will be posted publicly.'),css_class='col-sm-12 col-md-12'),
                css_class='form-row'
            ),
            Row(
                Column('anonymous', css_class='form-group col-sm-8 col-md-8'),
                Column(HTML(
                            '{% if request.user.is_reviewer %}' +
                                    'Review Status:  {{ review_status }} <br/>' +
                                    'Reviewer:  {{ reviewer_name }} <br/>' +
                                    'Submitter:  {{ submitter_name }}' +
                            '{% endif %}' 
                        ), 
                    css_class='form-group col-sm-4 col-md-4 text-primary font-weight-bold'),
                css_class='form-row'
            ),
            Accordion(
                AccordionGroup('Identification',
                    Row(
                        Column('levelOfAuthority', css_class='form-group col-sm-2 col-md-6'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('country', css_class='form-group col-sm-2 col-md-4'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('industry_type', css_class='form-group col-sm-2 col-md-4'),
                        Column('industry_type_other', css_class='form-group col-sm-2 col-md-4'),
                        css_class='form-row'
                    ),
                )
            ),
            Accordion(
                AccordionGroup('Summary',
                    Row(
                        Column('scenario_summary', css_class='form-group col-sm-4 col-md-12'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('bribe_initiator', css_class='form-group col-sm-2 col-md-3'),
                        Column('bribe_facilitator', css_class='form-group col-sm-2 col-md-3'),
                        Column('bribe_recipient', css_class='form-group col-sm-2 col-md-3'),
                        Column('bribe_type', css_class='form-group col-sm-2 col-md-3'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('bribe_initiator_other', css_class='form-group col-sm-2 col-md-3'),
                        Column('bribe_facilitator_other', css_class='form-group col-sm-2 col-md-3'),
                        Column('bribe_recipient_other', css_class='form-group col-sm-2 col-md-3'),
                        Column('bribe_type_other', css_class='form-group col-sm-2 col-md-3'),
                        css_class='form-row'
                    ),
                )
            ),
            Accordion(
                AccordionGroup('Scenario Details',
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
                )
            ),
            Accordion(
                AccordionGroup('Supporting Documents',
                    Row(
                        Column(HTML('<input type="file" multiple>'),css_class='col-sm-12 col-md-12'),
                        css_class='form-row'
                    ),
                    Row(
                        Column(
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

