import logging

from django.contrib.postgres.search import SearchVector
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Case, CharField, Value, When
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import IncidentForm, SearchForm, CreateUserForm
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

Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19
"""

logger = logging.getLogger(__name__)


"""
Example found at https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
Currently it's uploading the file to the root directory instead of in the /media folder.
The next video to watch is https://www.youtube.com/watch?v=KQJRwWpP8hs
"""
def upload(request):
    template = 'rlcis/upload.html'
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, template, context)

"""

Return all Incidents or search based on the returned Query from persistance.

Fields:
q -- Query returned from the user

"""
def incidents(request):
    template = 'rlcis/incident_list.html'
    query = request.GET.get('q')

    if not query:
        incident_list = Incident.objects.filter(scenario=False).order_by('-id')
    else:
        incident_list = __search(query).filter(scenario=False)

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
Incident Form used to create and update and Incident and persist.

Fields:
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
        context = {
            'form': form,
            'activePage': 'incidents',
            'id': id,
        }
        return render(request, 'rlcis/incident_form.html', context)
    else:
        if id == 0:
            logger.debug("starting incident_form - id = 0 POST")
            form = IncidentForm(request.POST)
        else:
            logger.debug("starting incident_form - id exist POST")
            incident = Incident.objects.get(pk=id)
            form = IncidentForm(request.POST, instance=incident)
        logger.debug(form.errors)
        if form.is_valid():
            logger.debug("starting incident_form - is valid save() POST")
            form.save()
            print('form submitted - RL')
        else:
            logger.debug(form.errors)
            logger.debug("form.is_valid() failed")
        return redirect('/rlcis/incidents/')


"""
Incident delete method used to remove an Incident from persisted store.

Fields:
id = incident id,  pk of incident to delete
"""
def incident_delete(request, id):
    logger.debug("trying to delete ")
    incident = Incident.objects.get(pk=id)
    logger.debug(incident)
    incident.delete()
    return redirect('/rlcis/incidents/')


"""
Return all scenarios or search based on the returned Query from persistance.

Fields:

q -- Query returned from the user
"""

def scenarios(request):
    template = 'rlcis/scenario_list.html'
    query = request.GET.get('q')

    if not query:
        incident_list = Incident.objects.filter(scenario=True).order_by('-id')
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


"""
Scenario method used to display specified scenario from persisted store

Fields:
id = scenario id,  pk of scenario to display

"""
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
        if form.is_valid():
            tempObj = form.save(commit=False)
            tempObj.scenario = True
            tempObj.save()
            logger.debug("starting scenario_form - is valid save() POST")
            form.save()
        else:
            logger.debug(form.errors)
            logger.debug("form.is_valid() failed")
        return redirect('/rlcis/scenarios/')

"""
Scenario delete method used to remove a scenario from persisted store.

Fields:
id = incident id,  pk of incident to delete
"""
def scenario_delete(request, id):
    logger.debug("trying to delete scenario")
    incident = Incident.objects.get(pk=id)
    logger.debug(incident)
    incident.delete()
    return redirect('scenarios/')

"""
private method used to search multiple Incident columns utilizing postgres SearchVector.

fields:

query -- contains the query to search Incidents against

"""
def __search(query):

    logger.debug("Query = " + query)
    incident_list = Incident.objects.annotate(
        industry_type_text=Case(  # used to search on the text values instead of the 2 character code stored in the database.
            *[When(industry_type=i, then=Value(v))
                   for i, v in Incident.INDUSTRY_TYPE_CHOICES],
            default=Value(''),
            output_field=CharField()
        ),
        bribed_by_text=Case(  # used to search on the text values instead of the 2 character code stored in the database.
            *[When(bribed_by=bb, then=Value(v))
                   for bb, v in Incident.BRIBED_BY_CHOICES],
            default=Value(''),
            output_field=CharField()
        ),
        bribe_type_text=Case(  # used to search on the text values instead of the 2 character code stored in the database.
            *[When(bribe_type=bt, then=Value(v))
                   for bt, v in Incident.BRIBE_TYPE_CHOICES],
            default=Value(''),
            output_field=CharField()
        ),
        search=SearchVector(
            'incident_summary',
            'incident_details',
            'country',
            'region',
            'location',
            'company_name',
            'industry_type_text',
            'bribed_by_text',
            'bribe_type_text',
        ),
    ).filter(search=query).order_by('-id')
    return incident_list

"""
Index method used to render index.html (home page)

"""
def index(request):
    return render(request, 'rlcis/index.html', {'activePage': 'home'})


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('rlcis:loginPage')

    context = {'form':form,
    'activePage': 'register'
    }


    return render(request, 'rlcis/accounts/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

  #  context = {}
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('rlcis:home')
        else:
            messages.info(request,'Username or Password is incorrect...')

    return render(request, 'rlcis/accounts/login.html', {'activePage': 'login'})

def logoutUser(request):
    logout(request)
    return redirect('rlcis:loginPage')
