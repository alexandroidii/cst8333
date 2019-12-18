from django.contrib.postgres.search import SearchVector
from django.core.paginator import(
    EmptyPage, PageNotAnInteger, Paginator,
)
from django.shortcuts import redirect, render

from .forms import IncidentForm, SearchForm
from .models import Incident

""" 
RLCIS Views that control the flow of information 
from the page to the database and back.

Functions:
incident_list -- a list of Incidents
incident_search -- a QuerySet list of Incidents
incident_form -- create and update Incident form
incident_delete -- deletes an Incident
index -- Home page for RLCIS
scenarios -- TODO create a model and pages for Scenarios

Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19
"""

"""
Verify if a query is being passed, and return either 
the full list of Incidents of a QuerySet based on the query.
 """
def incident_list(request):
    query = request.GET.get('query')
    if not query:
        incident_list = Incident.objects.all().order_by('-id')
    else:
        incident_list = __search(query)

    searchForm = SearchForm()
    paginator = Paginator(incident_list, 2)
    page = request.GET.get('page')
    try:
        incidents = paginator.page(page)
    except PageNotAnInteger:
        incidents = paginator.page(1)
    except EmptyPage:
        incidents = paginator.page(paginator.num_pages)

    context = {
        'incident_list': incidents,
        'activePage': 'incident',
        'searchForm': searchForm,
    }
    return render(request, 'rlcis/incident_list.html', context)

"""
Search Incidents based on the returned Query.

fields:

q -- Query returned from the user
"""
def incident_search(request):
    template = 'rlcis/incident_list.html'
    query = request.GET.get('q')

    if not query:
        incident_list = Incident.objects.all().order_by('-id')
    else:
        incident_list = __search(query)

    searchForm = SearchForm()
    paginator = Paginator(incident_list, 2)
    page = request.GET.get('page')
    try:
        incidents = paginator.page(page)
    except PageNotAnInteger:
        incidents = paginator.page(1)
    except EmptyPage:
        incidents = paginator.page(paginator.num_pages)

    context = {
        'incident_list': incidents,
        'activePage': 'incident',
        'searchForm': searchForm,
        'query': query,
    }
    return render(request, template, context)

"""
private method used to search multiple Incident columns.

fields:

query -- contains the query to search Incidents against
"""
def __search(query):

    print(query)
    incident_list = Incident.objects.annotate(
        search=SearchVector(
            'incident_summary',
            'incident_details',
            'country',
            'region',
            'location',
            # 'first_occurence',
            # 'resolution_date'
        ),
    ).filter(search=query).order_by('-id')
    return incident_list

"""
Incident Form used to create and update and Incident

If id=0, this is a new Incident to be added to the database
If id>0, this incident is being updated
"""
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
        return render(request, 'rlcis/incident_form.html', {'form': form, 'activePage': 'incident'})
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
