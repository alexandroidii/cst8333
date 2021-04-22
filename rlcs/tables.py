import django_tables2 as tables

from .models import Scenario

class ReviewerScenarioTable(tables.Table):
    class Meta:
        model = Scenario
        attrs = {"class": "table table-hover table-striped table-bordered"}
        #Clickable Row - Add class clickable-row and data-href=url
        row_attrs = {
            'data-href': lambda record: record.get_absolute_url,
            'class': 'clickable-row',
        }
        sequence = (
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
        sequence = (
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

    def render_email(self, value, record):
        return mask_column_value(self, value, record)

#Used to mask the column values when the Anonymous column is set to True
def mask_column_value(self, value, record):
    if self.request.user.groups.filter(name='reviewer' or 'admin').exists() or record.submitter == self.request.user:
        return value
    elif record.anonymous:
        return '---'
    else: 
        return value