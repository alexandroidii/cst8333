from django.shortcuts import redirect, render

from .forms import IncidentForm
from .models import Incident


def incident_list(request):
    context = {
        'incident_list': Incident.objects.all(),
        'activePage': 'incidents'
    }
    return render(request, 'rlcis/incident_list.html', context)


def incident_form(request, id=0):
    print("starting incident_form")
    if request.method == "GET":
        if id == 0:
            print("starting incident_form - id = 0")
            form = IncidentForm()
        else:
            print("starting incident_form - id exists")
            incident = Incident.objects.get(pk=id)
            form = IncidentForm(instance=incident)
        return render(request, 'rlcis/incident_form.html', {'form': form,'activePage': 'incidents'})
    else:
        if id == 0:
            print("starting incident_form - id = 0 POST")
            form = IncidentForm(request.POST)
        else:
            print("starting incident_form - id exist POST")
            incident = Incident.objects.get(pk=id)
            form = IncidentForm(request.POST, instance=incident)
        if form.is_valid():
            print("starting incident_form - is valid save() POST")
            form.save()
        else:
            print(form.errors)
            print("form.is_valid() failed")
        return redirect('/rlcis/list/')


def incident_delete(request, id):
    print("trying to delete ")
    incident = Incident.objects.get(pk=id)
    print(incident)
    incident.delete()
    return redirect('/rlcis/list/')

def index(request):
    return render(request, 'rlcis/index.html', {'activePage': 'home'})

def scenarios(request):
    return render(request, 'rlcis/scenarios.html', {'activePage': 'scenarios'})

def searchIncidents(request):
    return render(request, 'rlcis/searchIncidents.html', {'activePage': 'incidents'})
 