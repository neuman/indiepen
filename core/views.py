from django.views.generic.base import TemplateView
from django.http import Http404
from django.shortcuts import render_to_response

from api import v1_api
import core.models as cm

class IndexView(TemplateView):
    template_name = 'app.html'


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
        # Call the base implementation first to get a context
        context = super(ProjectView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        project = cm.Project.objects.get(id=self.kwargs['instance_id'])
        context['project'] = project
        context['total_pledged'] = project.get_total_pledged()
        return context

from django.views.generic import DetailView

class ProjectsView(TemplateView):
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProjectsView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['projects'] = cm.Project.objects.all()
        return context