import django_tables2 as tables

from .models import Scenario

class ScenarioTable(tables.Table):
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
            "first_occurence",
            "email",
            "submitted_date",
            "reviewer",
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
            "resolution_date",
            "is_reviewed",
            "reviewed_date",
            "submitter",
            "anonymous",
            "is_training_scenario",
            )

# This is how I can show the reviewer or not depending on the role.
    #def render_count(self, value):
    # if self.request.user.is_authenticated():
    #     return value
    # else:
    #     return '---'