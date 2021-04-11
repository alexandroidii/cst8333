import logging, json
import calendar
from datetime import datetime
from django.contrib.auth.decorators import permission_required
from django.contrib.postgres.search import SearchVector
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Case, CharField, Value, When
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.decorators import login_required
from users.models import Users
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncDay

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import ScenarioFormReviewer, ScenarioFormSubmitter, SearchForm, ScenarioDocumentForm
from .models import Scenario, ScenarioDocument
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.http import HttpResponse
from django_tables2 import RequestConfig, LazyPaginator
from .tables import ScenarioTable

from rlcis.decorator import already_authenticated_user, allowed_users

"""
RLCIS Views that control the flow of information
from the page to the database and back.

Functions:
scenario_list -- a list of Scenarios
scenario_search -- a QuerySet list of Scenarios
scenario_form -- create and update Scenario form
scenario_delete -- deletes an Scenario
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
    docToDel = get_object_or_404(ScenarioDocument, pk = docId)
    jsonData = json.dumps({
        'filename': docToDel.filename(),
        'id': docToDel.pk
    })

    docToDel.delete()

    return HttpResponse(jsonData, content_type='json')

@permission_required('users.is_reviewer')
def publish_scenario(request):
    print("you are a reviewer")
    pass



def ScenariosTableView(request):
    scenario_table = ScenarioTable(Scenario.objects.all())
    # scenario_table.paginate(page=request.GET.get("page", 1), per_page=25)
    RequestConfig(request, paginate={"per_page": 5}).configure(scenario_table)
    # paginator_class = LazyPaginator
    return HttpResponse(scenario_table.as_html(request))


"""

Return all Scenarios or search based on the returned Query from persistance.

Fields:
q -- Query returned from the user

"""
def scenarios(request):
    template = 'rlcis/scenario_list.html'
    query = request.GET.get('q')

    
    
    if not query:
        # Verify if the user is logged in
        # if request.user:
        #     # make sure they are a reviewer
        #     if request.user.has_perm('users.is_reviewer'):
        #         # Filter the list of scenarios assigned to the reviewer, and order by Assigned to reviewer, then by Null reviewer
        #         scenario_list = Scenario.objects.filter(reviewer=request.user).order_by('-id')
        #         scenario_list +=  Scenario.objects.filter(reviewer = not request.user).order_by('-id')
        #         scenario_list +=  Scenario.objects.filter(reviewer=None).order_by('-id')
        #     else:
        scenario_list = Scenario.objects.order_by('-id')
    else:
        scenario_list = __search(query).filter(scenario=True)

    searchForm = SearchForm()
    paginator = Paginator(scenario_list, 5)
    page = request.GET.get('page')
    try:
        scenarios = paginator.page(page)
    except PageNotAnInteger:
        scenarios = paginator.page(1)
    except EmptyPage:
        scenarios = paginator.page(paginator.num_pages)

    context = {
        'scenario_list': scenarios,
        'activePage': 'scenario',
        'searchForm': searchForm,
        'query': query,
    }
    return render(request, template, context)


"""
Save an scenario form using ajax
"""
def save_scenario(request, id=0, **kwargs):
    logger.debug("Saving Scenario form")
    
    is_reviewer = request.user.groups.filter(name='reviewer').exists()
    is_submitter = request.user.groups.filter(name='submitter').exists()
    
    if request.method == 'POST' and request.is_ajax():
        if is_reviewer:
            form = ScenarioFormReviewer(request.POST)
        else:
            form = ScenarioFormSubmitter(request.POST)

        response = {}
        id = int(request.POST.get('id'))
        if id == 0:
            logger.debug("starting scenario_form - id = 0 POST")
            if is_reviewer:
                form = ScenarioFormReviewer(request.POST)
            else:
                form = ScenarioFormSubmitter(request.POST)
        else:
            logger.debug("starting scenario_form - id exist POST")
            scenario = Scenario.objects.get(pk=id)
            if is_reviewer:
                form = ScenarioFormReviewer(request.POST, instance=scenario)
            else:
                form = ScenarioFormSubmitter(request.POST, instance=scenario)
        print(form.errors)
        logger.debug(form.errors)
        if form.is_valid():
           
            logger.debug("starting scenario_form - is valid save() POST")

            kwargs['domain'] = get_current_site(request)

            # First save the form
            savedScenario = form.save()

            fileLength = request.POST.get('fileLength')
            
            files = {}
            # Then loop through any files and save them with a link to the scenario.
            for file_num in range(0, int(fileLength)):
                scenarioDocument = ScenarioDocument.objects.create(
                    scenario=savedScenario,
                    document=request.FILES.get(f'document{file_num}')
                )

            messages.success(request, 'Submission has been accepted for review')  
            context = {}
            context.update(csrf(request))
            files = ScenarioDocument.objects.filter(scenario=savedScenario)
            context['files'] = files
            scenarioForm_html = render_crispy_form(form, context=context)
            response['activePage'] = 'scenarios'
            response['html'] = scenarioForm_html
            response['success'] = True

        else:
            logger.debug("form.is_valid() failed")
            logger.debug(form.errors)
            response['success'] = False
            context = {}
            context.update(csrf(request))
            scenarioForm_html = render_crispy_form(form, context=context)
            response['html'] = scenarioForm_html
            response['id'] = id
            
        return HttpResponse(json.dumps(response), content_type='application/json')

    if is_reviewer:
        form = ScenarioFormReviewer()
    else:
        form = ScenarioFormSubmitter()

    return render(request, 'scenario_form.html', {'form': form})


"""
Scenario Form used to create and update and Scenario and persist.

Fields:
If id=0, this is a new Scenario to be added to the database
If id>0, this scenario is being updated

"""
@already_authenticated_user
@allowed_users(allowed_roles=['submitter','reviewer','admin'])
def scenario_form(request, id=0):
    logger.debug("starting scenario_form")
    is_reviewer = request.user.groups.filter(name='reviewer').exists()
    is_submitter = request.user.groups.filter(name='submitter').exists()

    if request.method == "GET":
        if id == 0:
            logger.debug("starting scenario_form - id = 0")
            if is_reviewer:
                form = ScenarioFormReviewer()
            else:
                form = ScenarioFormSubmitter()

            context = {
                'form': form,
                'activePage': 'scenarios',
                'id': id,
            }
        else:
            logger.debug("starting scenario_form - id exists")
            scenario = Scenario.objects.get(pk=id)
            if is_reviewer:
                form = ScenarioFormReviewer(instance=scenario)
            else:
                form = ScenarioFormSubmitter(instance=scenario)
            files = ScenarioDocument.objects.filter(scenario=scenario)
            context = {
                'form': form,
                'files': files,
                'activePage': 'scenarios',
                'id': id,
            }
        return render(request, 'rlcis/scenario_form.html', context)
    else:
        fileLength = request.POST.get('fileLength')
        id = int(request.POST.get('id'))
        print(fileLength)
        logger.debug("fileLength = " + fileLength)
        if id == 0:
            logger.debug("starting scenario_form - id = 0 POST")
            if is_reviewer:
                form = ScenarioFormReviewer(request.POST)
            else:
                form = ScenarioFormSubmitter(request.POST)
        else:
            logger.debug("starting scenario_form - id exist POST")
            scenario = Scenario.objects.get(pk=id)
            if is_reviewer:
                form = ScenarioFormReviewer(request.POST, instance=scenario)
            else:
                form = ScenarioFormSubmitter(request.POST, instance=scenario)
        print(form.errors)
        logger.debug(form.errors)
        if form.is_valid():
            logger.debug("starting scenario_form - is valid save() POST")
            print('test')
            messages.info(request, f'New scenario from was submitted successfully')
            # First save the form
            savedScenario = form.save()
            
            # Then loop through any files and save them with a link to the scenario.
            for file_num in range(0, int(fileLength)):
                ScenarioDocument.objects.create(
                    scenario=savedScenario,
                    document=request.FILES.get(f'document{file_num}')
                )
        else:
            print(form.errors)
            logger.debug(form.errors)
            logger.debug("form.is_valid() failed")
            # Need to return the cleaned data back to the form but it doesn't exist in the DB yet.
            scenario = Scenario.objects.get(pk=id)

            if is_reviewer:
                form = ScenarioFormReviewer(instance=scenario)
            else:
                form = ScenarioFormSubmitter(instance=scenario)
            files = ScenarioDocument.objects.filter(scenario=scenario)
            context = {
                'form': form,
                'files': request.FILES,
                'activePage': 'scenarios',
                'id': id,
            }
            return render(request, 'rlcis/scenario_form.html', context)

        # ToDo: Maybe we don't redirect but show a successfully saved message and just reload the form?   
        return redirect('rlcis:scenarios')


"""
Scenario delete method used to remove an Scenario from persisted store.

Fields:
id = scenario id,  pk of scenario to delete
"""

@login_required #login required decorator
def scenario_delete(request, id):
    logger.debug("trying to delete ")

    scenario = Scenario.objects.get(pk=id)
    files = ScenarioDocument.objects.filter(scenario=scenario)
    for file in files:
        logger.debug(file)
        file.delete()

    logger.debug(scenario)
    scenario.delete()
    return redirect('rlcis:scenarios')


"""
Return all scenarios or search based on the returned Query from persistance.

Fields:

q -- Query returned from the user
"""

def scenarios_old(request):
    template = 'rlcis/scenario_list.html'
    query = request.GET.get('q')

    if not query:
        scenario_list = Scenario.objects.filter(scenario=True).order_by('-id')
    else:
        scenario_list = __search(query).filter(scenario=True)
    searchForm = SearchForm()
    paginator = Paginator(scenario_list, 2)
    page = request.GET.get('page')
    try:
        scenarios = paginator.page(page)
    except PageNotAnInteger:
        scenarios = paginator.page(1)
    except EmptyPage:
        scenarios = paginator.page(paginator.num_pages)

    context = {
        'scenario_list': scenarios,
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
def scenario_form_old(request, id=0):
    logger.debug("starting scenario_form")
    if request.method == "GET":
        if id == 0:
            logger.debug("starting scenario_form - id = 0")
            form = ScenarioFormReviewer()
        else:
            logger.debug("starting scenario_form - id exists")
            scenario = Scenario.objects.get(pk=id)
            form = ScenarioFormReviewer(instance=scenario)
        return render(request, 'rlcis/scenario_form.html', {'form': form, 'activePage': 'scenarios'})
    else:
        if id == 0:
            logger.debug("starting scenario_form - id = 0 POST")
            form = ScenarioFormReviewer(request.POST)
        else:
            logger.debug("starting scenario_form - id exist POST")
            scenario = Scenario.objects.get(pk=id)
            form = ScenarioFormReviewer(request.POST, instance=scenario)
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
private method used to search multiple Scenario columns utilizing postgres SearchVector.

fields:

query -- contains the query to search Scenarios against

"""
def __search(query):

    logger.debug("Query = " + query)
    scenario_list = Scenario.objects.annotate(
        industry_type_text=Case(  # used to search on the text values instead of the 2 character code stored in the database.
            *[When(industry_type=i, then=Value(v))
                   for i, v in Scenario.INDUSTRY_TYPE_CHOICES],
            default=Value(''),
            output_field=CharField()
        ),
        bribed_by_text=Case(  # used to search on the text values instead of the 2 character code stored in the database.
            *[When(bribed_by=bb, then=Value(v))
                   for bb, v in Scenario.BRIBED_BY_CHOICES],
            default=Value(''),
            output_field=CharField()
        ),
        bribe_type_text=Case(  # used to search on the text values instead of the 2 character code stored in the database.
            *[When(bribe_type=bt, then=Value(v))
                   for bt, v in Scenario.BRIBE_TYPE_CHOICES],
            default=Value(''),
            output_field=CharField()
        ),
        search=SearchVector(
            'scenario_summary',
            'scenario_details',
            'country',
            'region',
            'location',
            'company_name',
            'industry_type_text',
            'bribed_by_text',
            'bribe_type_text',
        ),
    ).filter(search=query).order_by('-id')
    return scenario_list

"""
Index method used to render index.html (home page)

"""
def index(request):
    tot_subs = Scenario.objects.count()
    scenarios = Scenario.objects.order_by('id')[:3]
    current_date = datetime.now()
    resolved_stats = Scenario.objects.annotate(month=TruncMonth('resolution_date')).values('month').annotate(total=Count('id'))
    month = calendar.month_name[current_date.month]
    year = current_date.year
    resolved = resolved_stats[0]['total']

    scenarios_this_month = Scenario.objects.filter(submitted_date__month=current_date.month,submitted_date__year=current_date.year ).count()

    context = {
        'scenarios': scenarios,
        'activePage': 'home',
        'month': month,
        'year': year,
        'total': scenarios_this_month,
        'resolved':resolved,
        'tot_subs':tot_subs
    }
    return render(request, 'rlcis/landing.html', context)


def about(request):
    return render(request, 'rlcis/about.html', {'activePage': 'about'})