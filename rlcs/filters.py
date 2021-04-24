from users.signals import User
from django import forms
from django.db import models
from django_filters.filters import ModelChoiceFilter
from rlcs.models_dropdown import BribeFacilitator, BribeInitiator, BribeRecipient, BribeType, IndustryType, LevelOfAuthority
from rlcs.forms import ReviewerScenarioFilterForm, SubmitterScenarioFilterForm
import django_filters
from .models import Scenario


"""
These filters are applied to the Tables.py classes in order to filter the data before returning it.

It also generates the filter form on the page that will allow users to filter columns manually.
"""
class ReviewerScenarioFilter(django_filters.FilterSet):
    industry_type = ModelChoiceFilter(queryset=IndustryType.objects.all(), empty_label=(''))
    bribe_initiator = ModelChoiceFilter(queryset=BribeInitiator.objects.all(), empty_label=(''))
    bribe_facilitator = ModelChoiceFilter(queryset=BribeFacilitator.objects.all(), empty_label=(''))
    bribe_recipient = ModelChoiceFilter(queryset=BribeRecipient.objects.all(), empty_label=(''))
    bribe_type = ModelChoiceFilter(queryset=BribeType.objects.all(), empty_label=(''))
    levelOfAuthority = ModelChoiceFilter(queryset=LevelOfAuthority.objects.all(), empty_label=(''))
    reviewer = ModelChoiceFilter(queryset=User.objects.all().filter(is_reviewer=True), empty_label=(''))
    is_reviewed = django_filters.BooleanFilter(field_name='is_reviewed')

    class Meta:
        model = Scenario
        form = ReviewerScenarioFilterForm
        fields = {
                    'country',
                    'region',
                    'location',
                    'company_name',
                    'scenario_summary',
                    'scenario_details',
                    'email',
                    'industry_type',
                    'levelOfAuthority',
                    'industry_type',
                    'bribe_initiator',
                    'bribe_facilitator',
                    'bribe_recipient',
                    'bribe_type',
                    'reviewer',
                    'submitted_date',
                    'is_reviewed',
                    'submitter',
        }
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.EmailField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }

                
class SubmitterScenarioFilter(django_filters.FilterSet):
    industry_type = ModelChoiceFilter(queryset=IndustryType.objects.all(), empty_label=(''))
    bribe_initiator = ModelChoiceFilter(queryset=BribeInitiator.objects.all(), empty_label=(''))
    bribe_facilitator = ModelChoiceFilter(queryset=BribeFacilitator.objects.all(), empty_label=(''))
    bribe_recipient = ModelChoiceFilter(queryset=BribeRecipient.objects.all(), empty_label=(''))
    bribe_type = ModelChoiceFilter(queryset=BribeType.objects.all(), empty_label=(''))
    levelOfAuthority = ModelChoiceFilter(queryset=LevelOfAuthority.objects.all(), empty_label=(''))
    reviewer = ModelChoiceFilter(queryset=User.objects.all().filter(is_reviewer=True), empty_label=(''))
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
                    'is_reviewed',
                    'submitter',
                ]
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }
        