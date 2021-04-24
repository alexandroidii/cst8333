import django_tables2 as tables
from django.utils.safestring import mark_safe

from .models import Scenario

"""
These table classes are used to render scenario tables which includes
pagination, sorting, and styling following a modelForm pattern.

There are different ones for Submitters and Reviewers with different fields being displayed.
"""
class ReviewerScenarioTable(tables.Table):
    class Meta:
        model = Scenario
        attrs = {"class": "table table-hover table-striped table-bordered"}
        #Clickable Row - Add class clickable-row and data-href=url
        row_attrs = {
            'data-href': lambda record: record.get_absolute_url,
            'class': 'clickable-row',
        }
        fields = (
            "id",
            "country",
            "company_name", 
            "industry_type",
            "scenario_summary",
            "bribe_type",
            "bribe_initiator",
            "bribe_facilitator",
            "bribe_recipient",
            "levelOfAuthority",
            "submitted_date",
            "first_occurence",
            "resolution_date",
            "email",
            "reviewer",
            'is_reviewed',
            )
        exclude = (
            "scenario_details", 
            "risks",
            "resolution",
            "bribe_initiator_other",
            "bribe_facilitator_other",
            "bribe_recipient_other",
            "bribed_by",
            "bribe_type_other",
            "industry_type_other",
            "reviewed_date",
            "submitter",
            "anonymous",
            "is_training_scenario",
            )

class SubmitterScenarioTable(tables.Table):
    class Meta:
        model = Scenario
        attrs = {"class": "table table-hover table-striped table-bordered"}
        #Clickable Row - Add class clickable-row and data-href=url
        row_attrs = {
            'data-href': lambda record: record.get_absolute_url,
            'class': 'clickable-row',
        }
        fields = (
            "id",
            "country",
            "company_name", 
            "industry_type",
            "scenario_summary",
            "bribe_type",
            "bribe_initiator",
            "bribe_facilitator",
            "bribe_recipient",
            "levelOfAuthority",
            "submitted_date",
            "first_occurence",
            "resolution_date",
            "email",
            )
        exclude = (
            "reviewer",
            'is_reviewed',
            "scenario_details", 
            "risks",
            "resolution",
            "bribe_initiator_other",
            "bribe_facilitator_other",
            "bribe_recipient_other",
            "bribed_by",
            "bribe_type_other",
            "industry_type_other",
            "reviewed_date",
            "submitter",
            "anonymous",
            "is_training_scenario",
            )


    def render_company_name(self, value, record):
        return mask_column_value(self, value, record)

    def render_region(self, value, record):
        return mask_column_value(self, value, record)
        
    def render_location(self, value, record):
        return mask_column_value(self, value, record)

    # Render the email address but hide it if record is marked anonymous.  
    # Had to use this method so the hover over email link wasn't displaying the public email.
    def render_email(self, value, record):
        email = None
        if self.request.user.groups.filter(name='reviewer' or 'admin').exists() or record.submitter == self.request.user:
            email = record.email
        elif record.anonymous:
            email = '---'
        else: 
            email = record.email
        email_link = "<a href='mailto:" + email + "'>" + email + "</a>"
        return mark_safe(email_link)

#Used to mask the column values when the Anonymous column is set to True
def mask_column_value(self, value, record):
    if self.request.user.groups.filter(name='reviewer' or 'admin').exists() or record.submitter == self.request.user:
        return value
    elif record.anonymous:
        return '---'
    else: 
        return value