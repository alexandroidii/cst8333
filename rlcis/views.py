from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .models import Incident


class IncidentList(ListView):
    model = Incident
    context_object_name = 'incidents'
    queryset = Incident.objects.all()
    template_name = 'rlcis/incident_list.html'


class IncidentDetails(DetailView):
    model = Incident
    context_object_name = 'incidents'
    template_name = 'rlcis/incident_details.html'


class IncidentCreate(CreateView):
    model = Incident
    fields = ['incident_summary']


class IncidentUpdate(UpdateView):
    model = Incident
    fields = [
        'country',
        'region',
        'bribed_by',
        'bribed_by_other',
        'bribe_type',
        'bribe_type_other',
        'location',
        'first_occurence',
        'resolution_date',
        'reviewer', ]


class IncidentDelete(DeleteView):
    model = Incident

    success_url = reverse_lazy('incident-list')


def index(request):
    return HttpResponse("Hello, world. You're at the RLCIS index.")


def incident(request):
    incident_list = Incident.objects.all()
    context = {
        'incident_list': incident_list
    }
    return render(request, 'rlcis/index.html', context)
