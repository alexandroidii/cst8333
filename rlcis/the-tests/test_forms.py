from django.test import TestCase

from rlcis.forms import IncidentForm

""" 
RLCIS test_forms defines the unittests for the Incident form.
Following the setUpTestData, 12 defined tests are used to valiadate
the Incident form.


Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19
"""
class IncidentFormTest(TestCase):
    
    def test_incident_form_incident_summary_field_label(self):
        form = IncidentForm()
        self.assertTrue(
            form.fields['incident_summary'].label == None
            or form.fields['incident_summary'].label == 'Incident Summary')
    
    def test_incident_form_incident_details_field_label(self):
        form = IncidentForm()
        self.assertTrue(
            form.fields['incident_details'].label == None
            or form.fields['incident_details'].label == 'Incident Details')
    
    def test_incident_form_country_field_label(self):
        form = IncidentForm()
        self.assertTrue(
            form.fields['country'].label == None
            or form.fields['country'].label == 'Country')
    
    def test_incident_form_region_field_label(self):
        form = IncidentForm()
        self.assertTrue(
            form.fields['region'].label == None
            or form.fields['region'].label == 'Region')
    
    def test_incident_form_location_field_label(self):
        form = IncidentForm()
        self.assertTrue(
            form.fields['location'].label == None
            or form.fields['location'].label == 'Location')
    
    def test_incident_form_bribed_by_field_label(self):
        form = IncidentForm()
        self.assertTrue(
            form.fields['bribed_by'].label == None
            or form.fields['bribed_by'].label == 'Bribed By')
    
    def test_incident_form_bribed_by_other_field_label(self):
        form = IncidentForm()
        self.assertTrue(
            form.fields['bribed_by_other'].label == None
            or form.fields['bribed_by_other'].label == 'Bribed By Other')
    
    def test_incident_form_bribe_type_field_label(self):
        form = IncidentForm()
        self.assertTrue(
            form.fields['bribe_type'].label == None
            or form.fields['bribe_type'].label == 'Bribe Type')
    
    def test_incident_form_bribe_type_other_field_label(self):
        form = IncidentForm()
        self.assertTrue(
            form.fields['bribe_type_other'].label == None
            or form.fields['bribe_type_other'].label == 'Bribe Type Other')
    
    def test_incident_form_first_occurence_field_label(self):
        form = IncidentForm()
        self.assertTrue(
            form.fields['first_occurence'].label == None
            or form.fields['first_occurence'].label == 'First Occurence')
    
    def test_incident_form_resolution_date_field_label(self):
        form = IncidentForm()
        self.assertTrue(
            form.fields['resolution_date'].label == None
            or form.fields['resolution_date'].label == 'Resolution Date')
    
    def test_incident_form_reviewer_field_label(self):
        form = IncidentForm()
        self.assertTrue(
            form.fields['reviewer'].label == None
            or form.fields['reviewer'].label == 'Reviewer')
