from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms

from .models import Incident


class DateInput(forms.DateInput):
    input_type = 'date'


class SearchForm(forms.Form):
    q = forms.CharField(
        label = 'Search',
        max_length = 200,
        help_text="Search for Summary, Details, or Location" ,
        )
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        helper.form_show_labels = False
        # self.helper.widgets = forms.TextInput(attrs={'placeholder':'Search for Summary, Details, or Location'})
        # self.helper.attrs = {
        #     'placeholder':'Search for Summary, Details, or Location',
        # }

        #     # Moving field labels into placeholders
        # layout = helper.layout = Layout()
        # for field_name, field in self.fields.items():
        #     layout.append(Field(field_name, placeholder='Search for Summary, Details, or Location'))
        #     helper.form_show_labels = False

class IncidentForm(forms.ModelForm):
    anonymous = forms.BooleanField(
        required=False, 
        label="Submit Anonymously?",
        widget=forms.CheckboxInput(attrs={'class': 'anonymousToggle'})
    ) #TODO disable company_name, Country, Region, Location

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

        ]
        labels = {
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
        }
        widgets = {
            'first_occurence': DateInput(),
            'resolution_date': DateInput(),
            'incident_details': forms.Textarea(attrs={'rows':2}),

        }

        def __init__(self, *args, **kwargs):
            super(IncidentForm, self).__init__(*args, **kwargs)
            self.fields['bribed_by'].empty_label = "select"
            self.fields['bribe_type'].empty_label = "select"
            self.fields['industry_type'].empty_label = "select"
            self.fields['bribed_by_other'].required = False
            self.fields['bribe_type_other'].required = False
            self.fields['industry_type_other'].required = False
            self.fields['company_name'].required = False
            self.fields['anonymous'].required = False
            self.fields['first_occurence'].required = False
            self.fields['resolution_date'].required = False
            self.fields['reviewer'].required = False
