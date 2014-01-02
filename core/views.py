from django.views.generic.base import TemplateView
from django.http import Http404
from django.shortcuts import render_to_response
from django.views.generic import DetailView

from actions.models import Actionable

from api import v1_api
import core.models as cm
import core.forms as cf

class IndexView(TemplateView):
    template_name = 'bootstrap.html'

class MessageView(TemplateView):
    template_name = 'message.html'
    message = 'Message goes here.'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MessageView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['message'] = self.message
        return context


class DetailView(TemplateView):
    template_name = 'index.html'

    def get_detail(self, pk):
        tr = v1_api.canonical_resource_for('project')

        try:
            project = tr.cached_obj_get(pk=pk)
        except cm.Project.DoesNotExist:
            raise Http404

        bundle = tr.full_dehydrate(tr.build_bundle(obj=project))
        data = bundle.data
        return data

    def get_context_data(self, **kwargs):
        base = super(DetailView, self).get_context_data(**kwargs)
        base['data'] = self.get_detail(base['params']['pk'])
        return base

class BootstrapView(TemplateView):
    template_name = 'bootstrap.html'

class ProjectView(TemplateView):
    template_name = 'project.html'

    def get_context_data(self, **kwargs):
        person = cm.Person.objects.get(user=self.request.user)
        # Call the base implementation first to get a context
        context = super(ProjectView, self).get_context_data(**kwargs)
        project = cm.Project.objects.get(id=self.kwargs['instance_id'])
        context['project'] = project
        context['available_actions'] = project.get_available_actions()
        context['total_pledged'] = project.get_total_pledged()
        return context


class ProjectsView(TemplateView, Actionable):
    template_name = 'list.html'

    def get_actions(self):
        return [
            cm.ProjectCreateAction()
            ]

    def get_context_data(self, **kwargs):
        person = cm.Person.objects.get(user=self.request.user)
        context = super(ProjectsView, self).get_context_data(**kwargs)
        context['projects'] = cm.Project.objects.all()
        context['available_actions'] = self.get_available_actions(person)
        return context

from django.views.generic.edit import FormView

class PledgeFormView(FormView):
    template_name = 'form.html'
    form_class = cf.PledgeForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PledgeFormView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['verb'] = "Pledge"
        return context 

from django.views.generic.edit import CreateView

class PledgeCreate(CreateView):
    model = cm.Pledge
    template_name = 'form.html'
    fields = ['ammount']
    success_url = '/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.person = cm.Person.objects.get(user=self.request.user)
        form.instance.project = cm.Project.objects.get(id=self.kwargs['instance_id'])
        return super(PledgeCreate, self).form_valid(form)

class ProjectCreate(CreateView):
    model = cm.Project
    template_name = 'form.html'
    fields = '__all__'
    success_url = '/'

    def get_form(self, form_class):
        # Initialize the form with initial values and the subscriber object
        # to be used in EmailPreferenceForm for populating fields
        return cf.ProjectForm(self.request.POST or None, self.request.FILES or None, initial=self.get_initial())

