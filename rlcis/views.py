import logging, json

from django.contrib.postgres.search import SearchVector
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Case, CharField, Value, When
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.decorators import login_required

from .forms import IncidentForm, SearchForm, DocumentForm
from .models import Incident, Document

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import IncidentForm, SearchForm, IncidentDocumentForm
from .models import Incident, IncidentDocument
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.http import HttpResponse
import json

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

implement model file: https://www.youtube.com/watch?v=KQJRwWpP8hs
Implement Class View to display documents: https://www.youtube.com/watch?v=HSn-e2snNc8

"""

def deleteDocument(request):
    if request.method != 'POST':
        raise Http404

    docId = request.POST.get('id', None)
    docToDel = get_object_or_404(IncidentDocument, pk = docId)
    jsonData = json.dumps({
        'filename': docToDel.filename(),
        'id': docToDel.pk
    })

    docToDel.delete()

    return HttpResponse(jsonData, content_type='json')

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
    paginator = Paginator(incident_list, 20)
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
Save an incident form using ajax
"""
def save_incident(request, id=0):
    logger.debug("Saving Incident form")
    if request.method == 'POST' and request.is_ajax():
        form = IncidentForm(request.POST)
        response = {}
        id = int(request.POST.get('id'))
        # print(fileLength)
        # logger.debug("fileLength = " + fileLength)
        if id == 0:
            logger.debug("starting incident_form - id = 0 POST")
            form = IncidentForm(request.POST)
        else:
            logger.debug("starting incident_form - id exist POST")
            incident = Incident.objects.get(pk=id)
            form = IncidentForm(request.POST, instance=incident)
        print(form.errors)
        logger.debug(form.errors)
        if form.is_valid():
           
            logger.debug("starting incident_form - is valid save() POST")

            # First save the form
            savedIncident = form.save()

            fileLength = request.POST.get('fileLength')
            # Then loop through any files and save them with a link to the incident.
            for file_num in range(0, int(fileLength)):
                IncidentDocument.objects.create(
                    incident=savedIncident,
                    document=request.FILES.get(f'document{file_num}')
                )
            print('form submitted - RL')
            csrf_context = {}
            csrf_context.update(csrf(request))
            incidentForm_html = render_crispy_form(form, context=csrf_context)
            response['html'] = incidentForm_html
            response['success'] = True

        else:
            logger.debug("form.is_valid() failed")
            logger.debug(form.errors)
            response['success'] = False
            csrf_context = {}
            csrf_context.update(csrf(request))
            incidentForm_html = render_crispy_form(form, context=csrf_context)
            response['html'] = incidentForm_html
            incident = Incident.objects.get(pk=id)
            files = IncidentDocument.objects.filter(incident=incident)
            response['files'] = request.FILES
            response['activePage'] = 'incidents'
            response['id'] = id
            
        return HttpResponse(json.dumps(response), content_type='application/json')
            
    form = IncidentForm()
    return render(request, 'incident_form.html', {'form': form})
    
                # print(form.errors)
                # Need to return the cleaned data back to the form but it doesn't exist in the DB yet.

                # The problem is this is triggered from an Ajax call so it goes into the 
                # success portion of the Ajax callback which calls the incidents. 
                #  need to find a way to reload the page with the incorrect data and validation
                # jsonData = json.dumps({
                #     'filename': docToDel.filename(),
                #     'id': docToDel.pk
                # })

    

                # return HttpResponse( content_type='json')
        # will try to follow this: https://www.codingforentrepreneurs.com/blog/ajaxify-django-forms
                # context = {
                #     'form': form,
                #     'files': request.FILES,
                #     'activePage': 'incidents',
                #     'id': id,
                # }
                # return render(request, 'rlcis/incident_form.html', context)

            # ToDo: Maybe we don't redirect but show a successfully saved message and just reload the form?   
            # return redirect('rlcis:incidents')

            
           
           
           
           
           
           
           
           
           
           
           
           
           
        #    form.save()
        #    response['success'] = True
        # else:
        #    response['success'] = False
        #    csrf_context = {}
        #    csrf_context.update(csrf(request))
        #    incidentForm_html = render_crispy_form(form, context=csrf_context)
        #    response['html'] = incidentForm_html
        # return HttpResponse(json.dumps(response), content_type='application/json')



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
            context = {
                'form': form,
                'activePage': 'incidents',
                'id': id,
            }
        else:
            logger.debug("starting incident_form - id exists")
            incident = Incident.objects.get(pk=id)
            form = IncidentForm(instance=incident)
            files = IncidentDocument.objects.filter(incident=incident)
            context = {
                'form': form,
                'files': files,
                'activePage': 'incidents',
                'id': id,
            }
        return render(request, 'rlcis/incident_form.html', context)
    else:
        fileLength = request.POST.get('fileLength')
        id = int(request.POST.get('id'))
        print(fileLength)
        logger.debug("fileLength = " + fileLength)
        if id == 0:
            logger.debug("starting incident_form - id = 0 POST")
            form = IncidentForm(request.POST)
        else:
            logger.debug("starting incident_form - id exist POST")
            incident = Incident.objects.get(pk=id)
            form = IncidentForm(request.POST, instance=incident)
        print(form.errors)
        logger.debug(form.errors)
        if form.is_valid():
            logger.debug("starting incident_form - is valid save() POST")
            print('test')
            messages.info(request, f'New incident from was submitted successfully')
            # First save the form
            savedIncident = form.save()
            
            # Then loop through any files and save them with a link to the incident.
            for file_num in range(0, int(fileLength)):
                IncidentDocument.objects.create(
                    incident=savedIncident,
                    document=request.FILES.get(f'document{file_num}')
                )
        else:
            print(form.errors)
            logger.debug(form.errors)
            logger.debug("form.is_valid() failed")
            # Need to return the cleaned data back to the form but it doesn't exist in the DB yet.
            incident = Incident.objects.get(pk=id)
            form = IncidentForm(instance=incident)
            files = IncidentDocument.objects.filter(incident=incident)

            # The problem is this is triggered from an Ajax call so it goes into the 
            # success portion of the Ajax callback which calls the incidents. 
            #  need to find a way to reload the page with the incorrect data and validation
            # jsonData = json.dumps({
            #     'filename': docToDel.filename(),
            #     'id': docToDel.pk
            # })

 

            # return HttpResponse( content_type='json')
    # will try to follow this: https://www.codingforentrepreneurs.com/blog/ajaxify-django-forms
            context = {
                'form': form,
                'files': request.FILES,
                'activePage': 'incidents',
                'id': id,
            }
            return render(request, 'rlcis/incident_form.html', context)

        # ToDo: Maybe we don't redirect but show a successfully saved message and just reload the form?   
        return redirect('rlcis:incidents')


"""
Incident delete method used to remove an Incident from persisted store.

Fields:
id = incident id,  pk of incident to delete
"""

@login_required #login required decorator
def incident_delete(request, id):
    logger.debug("trying to delete ")

    incident = Incident.objects.get(pk=id)
    files = IncidentDocument.objects.filter(incident=incident)
    for file in files:
        logger.debug(file)
        file.delete()

    logger.debug(incident)
    incident.delete()
    return redirect('rlcis:incidents')


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
@login_required #login required decorator
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
        return redirect('rlcis:scenarios')

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
    return redirect('rlcis:scenarios')

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

