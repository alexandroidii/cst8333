from rlcs.forms import ReviewerScenarioFilterForm, SubmitterScenarioFilterForm
import django_filters
from .models import Scenario

class ReviewerScenarioFilter(django_filters.FilterSet):
    class Meta:
        model = Scenario
        form = ReviewerScenarioFilterForm
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
                    'reviewer',
                    'email',
                    'submitted_date',
                ]
                
class SubmitterScenarioFilter(django_filters.FilterSet):
    class Meta:
        model = Scenario
        form = SubmitterScenarioFilterForm
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