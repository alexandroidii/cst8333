from django.test import TestCase

from rlcis.forms import IncidentForm

class IncidentFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        IncidentForm.objects.create(
            incident_summary='Django unittest summary',
            incident_details='Django unittest Details',
            country='Canada',
            region='Ontario',
            location='Ottawa',
            bribed_by='AG',
            bribed_by_other='',
            bribe_type='CA',
            bribe_type_other='',
            first_occurence='2019-12-17',
            resolution_date='2019-12-18',
            # reviewer',     Not sure if I need this or not
        )

        def test_country_field_equals(self):
            form = IncidentForm()
            self.assertEqual(form.fields['country'] == 'Canada')