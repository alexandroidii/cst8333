import logging, json
import calendar
from datetime import datetime
from django.contrib.auth.decorators import permission_required
from django.contrib.postgres.search import SearchVector
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Case, CharField, Value, When, Q
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

from .forms import ScenarioFormReviewer, ScenarioFormSubmitter, SearchForm, ScenarioDocumentForm, ReviewerScenarioFilterForm, SubmitterScenarioFilterForm
from .models import Scenario, ScenarioDocument
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.http import HttpResponse
from django_tables2 import RequestConfig, LazyPaginator
from .tables import ReviewerScenarioTable, SubmitterScenarioTable
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .filters import ReviewerScenarioFilter, SubmitterScenarioFilter
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Row, Column, HTML, Submit

from rlcs.decorator import already_authenticated_user, allowed_users

"""
RLCS Views that control the flow of information
from the page to the database and back.

Functions:
scenario_list -- a list of Scenarios
scenario_search -- a QuerySet list of Scenarios
scenario_form -- create and update Scenario form
scenario_delete -- deletes an Scenario
index -- Home page for RLCS

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

@already_authenticated_user
@allowed_users(allowed_roles=['reviewer'])
def publish_scenario(request, id):
    
    is_reviewer = request.user.groups.filter(name='reviewer' or 'admin').exists()
    is_submitter = request.user.groups.filter(name='submitter').exists()
    response = {}
    response['success'] = False
    scenario = Scenario.objects.get(pk=id)
    if request.method == 'POST' and request.is_ajax():
        if is_reviewer:
            form = ScenarioFormReviewer(request.POST, instance=scenario)
        else:
            form = ScenarioFormSubmitter(request.POST, instance=scenario)

    if form.is_valid():
           

        savedScenario = form.save(commit=False)
        if is_reviewer:
            savedScenario.is_reviewed = True
        else:
            print("You are not a reviewer and cannot publish this")

        savedScenario.save()

        messages.success(request, 'Scenario has been published.')  
        response['success'] = True

    return HttpResponse(json.dumps(response), content_type='application/json')



class FilteredScenarioListView(SingleTableMixin, FilterView):
    model = Scenario
    template_name = "rlcs/scenario_list.html"
    table_pagination = {'per_page': 5}
    
    def get(self, request, *args, **kwargs):
        is_reviewer = request.user.groups.filter(name='reviewer' or 'admin').exists()
        
        if is_reviewer:
            self.table_class = ReviewerScenarioTable
            self.table_data = Scenario.objects.order_by("-id")
            self.form_class = ReviewerScenarioFilterForm
            self.filterset_class = ReviewerScenarioFilter
        else:
            self.table_class = SubmitterScenarioTable
            # only show scenarios that have been reviewed and published, or scenarios that the user submitted.
            self.table_data = Scenario.objects.filter(Q(is_reviewed=True) | Q(submitter = request.user)).order_by("-id")
            self.form_class = SubmitterScenarioFilterForm
            self.filterset_class = SubmitterScenarioFilter

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activePage'] = 'scenarios'

        return context

"""
Save an scenario form using ajax
"""
@already_authenticated_user
@allowed_users(allowed_roles=['submitter','reviewer','admin'])
def save_scenario(request, id=0, **kwargs):
    logger.debug("Saving Scenario form")
    
    is_reviewer = request.user.groups.filter(name='reviewer' or 'admin').exists()
    
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
            savedScenario = form.save(commit=False)
            if is_reviewer:
                savedScenario.reviewer = request.user
            else:
                savedScenario.submitter = request.user
                if savedScenario.is_reviewed:
                    savedScenario.is_reviewed = False

            savedScenario.save()

            # First save the form

            fileLength = request.POST.get('fileLength')
            
            files = {}
            # Then loop through any files and save them with a link to the scenario.
            for file_num in range(0, int(fileLength)):
                scenarioDocument = ScenarioDocument.objects.create(
                    scenario=savedScenario,
                    document=request.FILES.get(f'document{file_num}')
                )
            if is_reviewer:
                messages.success(request, 'Scenario has been saved.')  
            else:
                messages.success(request, 'Scenario has been sent for review')  

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
def scenario_form(request, id=0, *args, **kwargs):
    logger.debug("starting scenario_form")
    is_reviewer = request.user.groups.filter(name='reviewer' or 'admin').exists()

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
            reviewer_name = None
            submitter_name = None
            review_status = None
            if is_reviewer:
                instance = (scenario)
                form = ScenarioFormReviewer(instance=instance)
                reviewer_name = scenario.reviewer
                submitter_name = scenario.submitter
                review_status = "Published" if scenario.is_reviewed else "Under Review"
            else:
                form = ScenarioFormSubmitter(instance=scenario)
                submitter_name = scenario.submitter
            files = ScenarioDocument.objects.filter(scenario=scenario)
            context = {
                'form': form,
                'files': files,
                'activePage': 'scenarios',
                'id': id,
                'reviewer_name': reviewer_name,
                'submitter_name': submitter_name,
                'review_status': review_status,
                'is_author': submitter_name.user_name == request.user.user_name if submitter_name and request.user.is_authenticated else False,
            }
        return render(request, 'rlcs/scenario_form.html', context)


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
    return redirect('rlcs:scenarios')


"""
Return all scenarios or search based on the returned Query from persistance.

Fields:

q -- Query returned from the user
"""

def scenarios_old(request):
    template = 'rlcs/scenario_list.html'
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
        return render(request, 'rlcs/scenario_form.html', {'form': form, 'activePage': 'scenarios'})
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
        return redirect('rlcs:scenarios')


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
    month = calendar.month_name[current_date.month]
    year = current_date.year
    if scenarios:
        resolved_stats = Scenario.objects.annotate(month=TruncMonth('resolution_date')).values('month').annotate(total=Count('id'))
        resolved = resolved_stats[0]['total']
        scenarios_this_month = Scenario.objects.filter(submitted_date__month=current_date.month,submitted_date__year=current_date.year ).count()
    else:
        resolved = 0
        scenarios_this_month = 0

    context = {
        'scenarios': scenarios,
        'activePage': 'home',
        'month': month,
        'year': year,
        'total': scenarios_this_month,
        'resolved':resolved,
        'tot_subs':tot_subs
    }
    return render(request, 'rlcs/landing.html', context)


def about(request):
    return render(request, 'rlcs/about.html', {'activePage': 'about'})