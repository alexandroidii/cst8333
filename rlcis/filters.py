from rlcis.forms import ScenarioFilterForm
import django_filters
from .models import Scenario

class ScenarioFilter(django_filters.FilterSet):
    class Meta:
        model = Scenario
        form = ScenarioFilterForm
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