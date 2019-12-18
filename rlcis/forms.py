from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
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
    class Meta:
        model = Incident
        fields = [
            'incident_summary',
            'incident_details',
            'country',
            'region',
            'bribed_by',
            'bribed_by_other',
            'bribe_type',
            'bribe_type_other',
            'location',
            'first_occurence',
            'resolution_date',
            'reviewer',
        ]
        labels = {
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
        }
        widgets = {
            'first_occurence': DateInput(),
            'resolution_date': DateInput(),
        }

        def __init__(self, *args, **kwargs):
            super(IncidentForm, self).__init__(*args, **kwargs)
            self.fields['bribed_by'].empty_label = "select"
            self.fields['bribe_type'].empty_label = "select"
            self.fields['bribed_by_other'].required = False
            self.fields['bribe_type_other'].required = False
            self.fields['first_occurence'].required = False
            self.fields['resolution_date'].required = False
            self.fields['reviewer'].required = False
