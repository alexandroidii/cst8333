import django_filters
from .models import Scenario

class ScenarioFilter(django_filters.FilterSet):
    class Meta:
        model = Scenario
        fields = [
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
                ]