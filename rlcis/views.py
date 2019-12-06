from django.shortcuts import redirect, render

from .forms import IncidentForm
from .models import Incident

# class IncidentList(ListView):
#     context_object_name = 'incidents'
#     queryset = Incident.objects.all()
#     template_name = 'rlcis/incident_list.html'


# class IncidentDetails(DetailView):
#     context_object_name = 'incidents'
#     queryset = Incident.objects.all()
#     template_name = 'rlcis/incident_details.html'


# class IncidentCreate(CreateView):
#     model = Incident
#     fields = ['incident_summary']


# class IncidentUpdate(UpdateView):
#     model = Incident
#     fields = [
#         'country',
#         'region',
#         'bribed_by',
#         'bribed_by_other',
#         'bribe_type',
#         'bribe_type_other',
#         'location',
#         'first_occurence',
#         'resolution_date',
#         'reviewer', ]


# class IncidentDelete(DeleteView):
#     model = Incident

#     success_url = reverse_lazy('incident-list')

def incident_list(request):
    context = {
        'incident_list': Incident.objects.all()
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
        return render(request, 'rlcis/incident_form.html', {'form': form})
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
