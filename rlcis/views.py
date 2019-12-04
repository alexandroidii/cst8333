from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader

from .models import Incident


def index(request):
    return HttpResponse("Hello, world. You're at the RLCIS index.")


def incident(request):
    incident_list = Incident.objects.all()
    context = {
        'incident_list': incident_list
    }
    return render(request, 'rlcis/index.html', context)


def scenerio(request, incident_id):
    try:
        incident = get_object_or_404(Incident, pk=incident_id)
        return render(request, 'rlcis/incident.html', {'incident': incident})
