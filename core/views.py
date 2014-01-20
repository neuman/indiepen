from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.http import Http404
from django.shortcuts import render_to_response
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from uuid import uuid4

from actions.models import Actionable

from api import v1_api
import core.models as cm
import core.forms as cf


from django.db.models.signals import post_save
from actstream import action
from actstream.models import user_stream, action_object_stream, model_stream, actor_stream

from django.contrib.auth import authenticate, login



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
    template_name = 'grid.html'
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

class StreamListView(TemplateView, Actionable):
    template_name = 'stream.html'

    def get_context_data(self, **kwargs):

        context = super(StreamListView, self).get_context_data(**kwargs)
        object_type = ContentType.objects.get(app_label="core", model=self.kwargs['instance_model']).model_class()
        object_instance = get_object_or_404(object_type, pk=self.kwargs['instance_id'])
        context['object_instance'] = object_instance
        context['available_actions'] = object_instance.get_available_actions(self.request.user)
        context['stream'] = object_instance.action_object_actions.all()
        return context

class ProjectDetailView(TemplateView):
    template_name = 'project.html'

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project = cm.Project.objects.get(id=self.kwargs['instance_id'])
        context['project'] = project
        context['available_actions'] = project.get_available_actions(self.request.user)
        context['total_pledged'] = project.get_total_pledged()
        return context


class ProjectListView(TemplateView, Actionable):
    template_name = 'list.html'

    def get_actions(self):
        return [
            cm.ProjectCreateAction()
            ]

    def get_context_data(self, **kwargs):

        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['projects'] = cm.Project.objects.all()
        context['available_actions'] = self.get_available_actions(self.request.user)
        return context

from django.views.generic.edit import FormView

#Pledge STARTS
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
    fields = ['value']
    form = cf.PledgeForm

    def form_valid(self, form):
        form.instance.changed_by = self.request.user
        form.instance.pledger = self.request.user
        form.instance.project = cm.Project.objects.get(id=self.kwargs['instance_id'])
        return super(PledgeCreateView, self).form_valid(form)

    def get_success_url(self):
        #new_options = cm.Options.objects.create(user=self.request.user)
        #new_options.save()
        action.send(self.request.user, verb='pledged', action_object=self.object, target=self.object.project)
        return '/'
#Pledge ENDS

class ProjectCreateView(CreateView):
    model = cm.Project
    template_name = 'form.html'
    fields = '__all__'
    success_url = '/'
    form = cf.ProjectForm

    def get_success_url(self):
        self.object.members.add(self.request.user)
        action.send(self.request.user, verb='created', action_object=self.object)
        return reverse(viewname='project_detail', args=(self.object.id,), current_app='core')

class MediaCreateView(CreateView):
    model = cm.Media
    template_name = 'form.html'
    fields = '__all__'
    success_url = '/'

    def get_form(self, form_class):
        return cf.MediaForm(self.request.POST or None, self.request.FILES or None, initial=self.get_initial())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.changed_by = self.request.user
        action.send(self.request.user, verb='uploaded', action_object=self.object)
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
        form.instance.user = self.request.user
        form.instance.project = cm.Project.objects.get(id=self.kwargs['instance_id'])
        form.instance.changed_by = self.request.user
        self.instance = form.instance
        return super(PostCreateView, self).form_valid(form)

    def get_success_url(self):
        action.send(self.request.user, verb='posted', action_object=self.object, target=self.object.project)
        return reverse(viewname='post_media_uploads', args=(self.object.id,), current_app='core')

class PostUpdateView(UpdateView):
    model = cm.Post
    template_name = 'form.html'
    success_url = '/'

    def get_form(self, form_class):
        return cf.PostForm(self.request.POST or None, self.request.FILES or None, initial=self.get_initial())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = cm.Project.objects.get(id=self.kwargs['instance_id'])
        form.instance.changed_by = self.request.user
        return super(PostCreateView, self).form_valid(form)

class PostDetailView(TemplateView):
    template_name = 'media.html'

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post = cm.Post.objects.get(id=self.kwargs['instance_id'])
        context['post'] = post
        context['medias'] = post.get_medias()
        context['available_actions'] = post.get_available_actions(post)
        stream = []
        for a in action_object_stream(post):
            stream.append(a)
        for m in post.media.all():
            for a in action_object_stream(m):
                stream.append(a)
        context['stream'] = stream
        return context

class PostListView(TemplateView, Actionable):
    template_name = 'posts.html'

    def get_context_data(self, **kwargs):

        context = super(PostListView, self).get_context_data(**kwargs)
        context['posts'] = cm.Post.objects.all().order_by('-updated_at')
        context['available_actions'] = self.get_available_actions(self.request.user)
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
        #form.instance.user = self.request.user

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
        form.instance.changed_by = self.request.user

        self.new_instance = form.instance
        return super(PostMediaCreateView, self).form_valid(form)

    def get_success_url(self):
        p = cm.Post.objects.get(id=self.kwargs['instance_id'])
        p.media.add(self.new_instance)
        action.send(self.request.user, verb='uploaded', action_object=self.new_instance, target=p)
        return reverse(viewname='post_media_create', args=(self.kwargs['instance_id'],), current_app='core')

    def get_actions(self):
        return [
            cm.PostDetailAction(cm.Post.objects.get(id=self.kwargs['instance_id']))
            ]

    def get_context_data(self, **kwargs):

        context = super(PostMediaCreateView, self).get_context_data(**kwargs)
        context['available_actions'] = self.get_available_actions(self.request.user)
        return context

class PostUploadsView(TemplateView, Actionable):
    template_name = 'uploads.html'

    def get_actions(self):
        return [
            cm.PostDetailAction(cm.Post.objects.get(id=self.kwargs['instance_id']))
            ]

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(PostUploadsView, self).get_context_data(**kwargs)
        context['upload_url'] = reverse(viewname='post_media_create', args=(self.kwargs['instance_id'],), current_app='core')
        context['available_actions'] = self.get_available_actions(self.request.user)
        return context

#Post ENDS

#User STARTS 

class UserDetailView(TemplateView, Actionable):
    template_name = 'user.html'

    def get_actions(self):
        return [
            #cm.PostDetailAction(cm.Post.objects.get(id=self.kwargs['instance_id']))
            ]

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['instance_id'])
        context['user'] = user
        context['available_actions'] = None
        context['stream'] = actor_stream(user)
        return context

class UserCreateView(CreateView):
    model = User
    template_name = 'form.html'
    form_class = cf.RegistrationForm

    def form_valid(self, form):
        user = User.objects.create_user(uuid4().hex, form.cleaned_data['email'], form.cleaned_data['password1'])
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['first_name']
        user.save()
        user = authenticate(username=user.username, password=form.cleaned_data['password1'])
        login(self.request, user)
        form.instance = user
        return super(UserCreateView, self).form_valid(form)

    def get_success_url(self):
        action.send(self.request.user, verb='joined', action_object=self.object)
        return reverse(viewname='user_detail', args=(self.object.id,), current_app='core')

class UserLoginView(FormView):
    template_name = 'form.html'
    form_class = cf.LoginForm

    def form_valid(self, form):
        user = form.user_cache
        login(self.request, user)
        form.instance = user
        return super(UserLoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse(viewname='user_detail', args=(self.object.id,), current_app='core')
#User ENDS

#media STARTS
class MediaDetailView(TemplateView):
    template_name = 'media.html'

    def get_context_data(self, **kwargs):
        context = super(MediaDetailView, self).get_context_data(**kwargs)
        media = cm.Media.objects.get(id=self.kwargs['instance_id'])
        context['medias'] = [media]
        context['available_actions'] = media.get_available_actions(self.request.user)
        context['focus'] = True
        return context

class MediaListView(TemplateView):
    template_name = 'media.html'

    def get_context_data(self, **kwargs):
        context = super(MediaListView, self).get_context_data(**kwargs)
        context['medias'] = cm.Media.objects.all()
        #context['available_actions'] = media.get_available_actions(self.request.user)
        return context

from django_remote_forms.forms import RemoteForm
import json
from django.http import HttpResponse


class MediaUpdateView(UpdateView):
    model = cm.Media
    template_name = 'form.html'
    form_class = cf.MediaUpdateForm

    def get_context_data(self, **kwargs):
        context = super(MediaUpdateView, self).get_context_data(**kwargs)
        context['medias'] = [self.object]
        context['available_actions'] = self.object.get_available_actions(self.request.user)
        return context

    def get_success_url(self):
        post = cm.get_media_post(self.object)
        return post.get_absolute_url()

    def get(self, request, *args, **kwargs):
        supes = super(MediaUpdateView, self).get(request, *args, **kwargs)
        context = self.get_context_data(**kwargs)
        if self.request.is_ajax():
            remote_form = RemoteForm(self.get_form(self.form_class))
            blob = {
                'form':remote_form.as_dict(),
                'available_actions':self.object.get_available_actions(self.request.user),
                'object_instance':None
            }
            data = json.dumps(blob)
            out_kwargs = {'content_type':'application/json'}
            return HttpResponse(data, **out_kwargs)

        return supes

#media ENDS