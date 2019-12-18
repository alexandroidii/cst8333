from django.test import TestCase

from rlcis.forms import IncidentForm


class IncidentFormTest(TestCase):
    def test_incident_form_country_field_label(self):
        form = IncidentForm()
        self.assertTrue(
            form.fields['country'].label == None
            or form.fields['country'].label == 'Country')
