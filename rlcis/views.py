import logging

from django.contrib.postgres.search import SearchVector
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
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
logger = logging.getLogger(__name__)

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
        incident_list = Incident.objects.filter(scenario=False).order_by('-id')
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

    logger.debug("Query = " + query)
    incident_list = Incident.objects.annotate(
        search=SearchVector(
            'incident_summary',
            'incident_details',
            'country',
            'region',
            'location',
            'company',
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
    logger.debug("starting incident_form")
    if request.method == "GET":
        if id == 0:
            logger.debug("starting incident_form - id = 0")
            form = IncidentForm()
        else:
            logger.debug("starting incident_form - id exists")
            incident = Incident.objects.get(pk=id)
            form = IncidentForm(instance=incident)
        return render(request, 'rlcis/incident_form.html', {'form': form, 'activePage': 'incident'})
    else:
        if id == 0:
            logger.debug("starting incident_form - id = 0 POST")
            form = IncidentForm(request.POST)
        else:
            logger.debug("starting incident_form - id exist POST")
            incident = Incident.objects.get(pk=id)
            form = IncidentForm(request.POST, instance=incident)
        print(form.errors)
        if form.is_valid():
            logger.debug("starting incident_form - is valid save() POST")
            form.save()
        else:
            logger.debug(form.errors)
            logger.debug("form.is_valid() failed")
        return redirect('/rlcis/incidents/')


def incident_delete(request, id):
    logger.debug("trying to delete ")
    incident = Incident.objects.get(pk=id)
    logger.debug(incident)
    incident.delete()
    return redirect('/rlcis/incidents/')


def index(request):
    return render(request, 'rlcis/index.html', {'activePage': 'home'})


def scenario_list(request):

    query = request.GET.get('query')
    if not query:
        incident_list = Incident.objects.all().order_by('-id') #TODO filter this by scenario boolean
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
        'activePage': 'scenarios',
        'searchForm': searchForm,
    }

    return render(request, 'rlcis/scenario_list.html', context)

def scnario_search(request):
    template = 'rlcis/scenario_list.html'
    query = request.GET.get('q')

    if not query:
        incident_list = Incident.objects.all().order_by('-id')
    else:
        incident_list = __search(query).filter(scenario=True)

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
        'activePage': 'scenarios',
        'searchForm': searchForm,
        'query': query,
    }
    return render(request, template, context)


def scenario_form(request, id=0):
    logger.debug("starting scenario_form")
    if request.method == "GET":
        if id == 0:
            logger.debug("starting scenario_form - id = 0")
            form = IncidentForm()
        else:
            logger.debug("starting scenario_form - id exists")
            incident = Incident.objects.get(pk=id)
            form = IncidentForm(instance=incident)
        return render(request, 'rlcis/scenario_form.html', {'form': form, 'activePage': 'scenarios'})
    else:
        if id == 0:
            logger.debug("starting scenario_form - id = 0 POST")
            form = IncidentForm(request.POST)
        else:
            logger.debug("starting scenario_form - id exist POST")
            incident = Incident.objects.get(pk=id)
            form = IncidentForm(request.POST, instance=incident)
        print(form.errors)
        print('before form is valid = ' + str(form.is_valid()))
        request.POST._mutable = True
        form.data['scenario'] = True
        print('after form is valid = ' + str(form.is_valid()))
        if form.is_valid():
            logger.debug("starting scenario_form - is valid save() POST")
            # form.cleaned_data['scenario'] = True #TODO The value is not being saved to the database
            print(form.cleaned_data['scenario'])
            form.save()
        else:
            logger.debug(form.errors)
            logger.debug("form.is_valid() failed")
        return redirect('/rlcis/scenarios/')

def scenario_delete(request, id):
    logger.debug("trying to delete scenario")
    incident = Incident.objects.get(pk=id)
    logger.debug(incident)
    incident.delete()
    return redirect('scenarios/')
