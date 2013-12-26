from django.views.generic.base import TemplateView
from django.http import Http404

from api import v1_api
from .models import Project

class IndexView(TemplateView):
    template_name = 'index.html'


class DetailView(TemplateView):
    template_name = 'index.html'

    def get_detail(self, pk):
        tr = v1_api.canonical_resource_for('project')

        try:
            project = tr.cached_obj_get(pk=pk)
        except Project.DoesNotExist:
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