import django_tables2 as tables

from .models import Scenario

class ScenarioTable(tables.Table):
    class Meta:
        model = Scenario