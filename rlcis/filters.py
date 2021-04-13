import django_filters

from .models import Scenario

class ScenarioFilter(django_filters.FilterSet):
    class Meta:
        model = Scenario
        fields = '__all__'
        exclude = ['']