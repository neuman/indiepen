from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.http import Http404
from django.shortcuts import render_to_response
from django.views.generic import DetailView
from django.core.urlresolvers import reverse

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

class ProjectDetailView(TemplateView):
    template_name = 'project.html'

    def get_context_data(self, **kwargs):
        person = cm.Person.objects.get(user=self.request.user)
        # Call the base implementation first to get a context
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project = cm.Project.objects.get(id=self.kwargs['instance_id'])
        context['project'] = project
        context['available_actions'] = project.get_available_actions(person)
        context['total_pledged'] = project.get_total_pledged()
        return context


class ProjectListView(TemplateView, Actionable):
    template_name = 'list.html'

    def get_actions(self):
        return [
            cm.ProjectCreateAction()
            ]

    def get_context_data(self, **kwargs):
        person = cm.Person.objects.get(user=self.request.user)
        context = super(ProjectListView, self).get_context_data(**kwargs)
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


class PledgeCreateView(CreateView):
    model = cm.Pledge
    template_name = 'form.html'
    fields = ['ammount']
    success_url = '/'


    def get_form(self, form_class):
        return cf.PledgeForm(self.request.POST or None, self.request.FILES or None, initial=self.get_initial())

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.person = cm.Person.objects.get(user=self.request.user)
        form.instance.project = cm.Project.objects.get(id=self.kwargs['instance_id'])
        return super(PledgeCreate, self).form_valid(form)

class ProjectCreateView(CreateView):
    model = cm.Project
    template_name = 'form.html'
    fields = '__all__'
    success_url = '/'

    def get_form(self, form_class):
        return cf.ProjectForm(self.request.POST or None, self.request.FILES or None, initial=self.get_initial())

    def get_success_url(self):
        person = cm.Person.objects.get(user=self.request.user)
        self.object.members.add(person)
        return reverse(viewname='project_detail', args=(self.object.id,), current_app='core')

class MediaCreateView(CreateView):
    model = cm.Media
    template_name = 'form.html'
    fields = '__all__'
    success_url = '/'

    def get_form(self, form_class):
        return cf.MediaForm(self.request.POST or None, self.request.FILES or None, initial=self.get_initial())

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.person = cm.Person.objects.get(user=self.request.user)
        return super(MediaCreateView, self).form_valid(form)


#Post STARTS
class PostCreateView(CreateView):
    model = cm.Post
    template_name = 'form.html'
    success_url = '/'
    instance = None

    def get_form(self, form_class):
        return cf.PostForm(self.request.POST or None, self.request.FILES or None, initial=self.get_initial())

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.person = cm.Person.objects.get(user=self.request.user)
        form.instance.project = cm.Project.objects.get(id=self.kwargs['instance_id'])
        self.instance = form.instance
        return super(PostCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse(viewname='post_media_create', args=(self.object.id,), current_app='core')


class PostUpdateView(UpdateView):
    model = cm.Post
    template_name = 'form.html'
    success_url = '/'

    def get_form(self, form_class):
        return cf.PostForm(self.request.POST or None, self.request.FILES or None, initial=self.get_initial())

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.person = cm.Person.objects.get(user=self.request.user)
        form.instance.project = cm.Project.objects.get(id=self.kwargs['instance_id'])
        return super(PostCreateView, self).form_valid(form)

class PostDetailView(TemplateView):
    template_name = 'post.html'

    def get_context_data(self, **kwargs):
        person = cm.Person.objects.get(user=self.request.user)
        # Call the base implementation first to get a context
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post = cm.Post.objects.get(id=self.kwargs['instance_id'])
        context['post'] = post
        context['available_actions'] = post.get_available_actions(post)
        return context

class PostListView(TemplateView, Actionable):
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        person = cm.Person.objects.get(user=self.request.user)
        context = super(PostListView, self).get_context_data(**kwargs)
        context['projects'] = cm.Project.objects.all()
        context['available_actions'] = self.get_available_actions(person)
        return context

class PostMediaCreateView(CreateView, Actionable):
    model = cm.Media
    template_name = 'form.html'
    fields = '__all__'
    new_instance = None
    

    def get_form(self, form_class):
        return cf.MediaCreateForm(self.request.POST or None, self.request.FILES or None, initial=self.get_initial())

    def form_valid(self, form):
        #form.instance.created_by = self.request.user
        #form.instance.person = cm.Person.objects.get(user=self.request.user)

        def get_file_extension(string_in):
            #return string_in.__getslice__(string_in.__len__()-3, string_in.__len__()).lower()
            i = string_in.rfind(".")
            return string_in.__getslice__(i+1, string_in.__len__()).lower()

        def get_medium(extension_in):
            for medium in cm.EXTENSIONS:
                for extension in cm.EXTENSIONS[medium]:
                    if extension == extension_in:
                        return medium

        form.instance.medium = get_medium(get_file_extension(form.instance.original_file.name))

        self.new_instance = form.instance
        return super(PostMediaCreateView, self).form_valid(form)

    def get_success_url(self):
        p = cm.Post.objects.get(id=self.kwargs['instance_id'])
        p.media.add(self.new_instance)
        return reverse(viewname='post_media_create', args=(self.kwargs['instance_id'],), current_app='core')

    def get_actions(self):
        return [
            cm.PostDetailAction(cm.Post.objects.get(id=self.kwargs['instance_id']))
            ]

    def get_context_data(self, **kwargs):
        person = cm.Person.objects.get(user=self.request.user)
        context = super(PostMediaCreateView, self).get_context_data(**kwargs)
        context['available_actions'] = self.get_available_actions(person)
        return context

#Post ENDS

