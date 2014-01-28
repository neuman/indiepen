from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.http import Http404
from django.shortcuts import render_to_response
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from uuid import uuid4

from carteblanche.models import Noun

from api import v1_api
import core.models as cm
import core.forms as cf
import core.decorators as cd
import core.verbs as cv


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

class StreamListView(cv.RequiredVerbsAvailable, TemplateView):
    template_name = 'stream.html'

    def get_context_data(self, **kwargs):
        context = super(StreamListView, self).get_context_data(**kwargs)
        object_instance = self.noun
        context['object_instance'] = object_instance
        context['available_verbs'] = object_instance.get_available_verbs(self.request.user)
        context['stream'] = object_instance.action_object_actions.all()
        return context

    def get_noun(self, **kwargs):
        object_type = ContentType.objects.get(app_label="core", model=self.kwargs['instance_model']).model_class()
        return get_object_or_404(object_type, pk=self.kwargs['instance_id'])

class ProjectDetailView(cv.RequiredVerbsAvailable, TemplateView):
    template_name = 'project.html'

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project = self.noun
        context['project'] = project
        context['available_verbs'] = project.get_available_verbs(self.request.user)
        context['total_pledged'] = project.get_total_pledged()
        return context

    def get_noun(self, **kwargs):
        return cm.Project.objects.get(id=self.kwargs['instance_id'])


class ProjectListView(TemplateView, Noun):
    template_name = 'list.html'

    def get_verbs(self):
        return [
            cm.ProjectCreateVerb()
            ]

    def get_context_data(self, **kwargs):

        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['projects'] = cm.Project.objects.all()
        context['available_verbs'] = self.get_available_verbs(self.request.user)
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

class PledgeCreateView(cv.RequiredVerbsAvailable, CreateView):
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

    def dispatch(self, *args, **kwargs):
        self.noun = cm.Project.objects.get(id=self.kwargs['instance_id'])
        return super(PledgeCreateView, self).dispatch(*args, **kwargs)
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

class MediaCreateView(cv.RequiredVerbsAvailable, CreateView):
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

    def get_noun(self, **kwargs):
        return cm.Project.objects.get(id=self.kwargs['instance_id'])


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

class PostDetailView(cv.RequiredVerbsAvailable, TemplateView):
    template_name = 'media.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post = self.noun
        context['post'] = post
        context['medias'] = post.get_medias()
        context['available_verbs'] = post.get_available_verbs(self.request.user)
        stream = []
        for a in action_object_stream(post):
            stream.append(a)
        for m in post.media.all():
            for a in action_object_stream(m):
                stream.append(a)
        context['stream'] = stream
        return context

    def get_noun(self, **kwargs):
        return cm.Post.objects.get(id=self.kwargs['instance_id'])

class PostListView(TemplateView, Noun):
    template_name = 'posts.html'

    def get_context_data(self, **kwargs):

        context = super(PostListView, self).get_context_data(**kwargs)
        context['posts'] = cm.Post.objects.all().order_by('-updated_at')
        context['available_verbs'] = self.get_available_verbs(self.request.user)
        return context

class PostMediaCreateView(CreateView, Noun):
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

    def get_verbs(self):
        return [
            cm.PostDetailVerb(cm.Post.objects.get(id=self.kwargs['instance_id']))
            ]

    def get_context_data(self, **kwargs):

        context = super(PostMediaCreateView, self).get_context_data(**kwargs)
        context['available_verbs'] = self.get_available_verbs(self.request.user)
        return context

class PostUploadsView(cv.RequiredVerbsAvailable, TemplateView):
    template_name = 'uploads.html'

    def get_verbs(self):
        return [
            cm.PostDetailVerb(cm.Post.objects.get(id=self.kwargs['instance_id']))
            ]

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(PostUploadsView, self).get_context_data(**kwargs)
        context['upload_url'] = reverse(viewname='post_media_create', args=(self.kwargs['instance_id'],), current_app='core')
        return context

    def get_noun(self, **kwargs):
        return cm.Post.objects.get(id=self.kwargs['instance_id'])

#Post ENDS

#User STARTS 

class UserDetailView(TemplateView, Noun):
    template_name = 'user.html'

    def get_verbs(self):
        return [
            #cm.PostDetailVerb(cm.Post.objects.get(id=self.kwargs['instance_id']))
            ]

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['instance_id'])
        context['user'] = user
        context['available_verbs'] = None
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
class MediaDetailView(cv.RequiredVerbsAvailable, TemplateView):
    template_name = 'media.html'

    def get_context_data(self, **kwargs):
        context = super(MediaDetailView, self).get_context_data(**kwargs)
        media = self.noun
        context['medias'] = [media]
        context['available_verbs'] = media.get_available_verbs(self.request.user)
        context['focus'] = True
        return context

    def get_noun(self, **kwargs):
        return cm.Media.objects.get(id=self.kwargs['instance_id'])

class MediaListView(TemplateView):
    template_name = 'media.html'

    def get_context_data(self, **kwargs):
        context = super(MediaListView, self).get_context_data(**kwargs)
        context['medias'] = cm.Media.objects.all()
        #context['available_verbs'] = media.get_available_verbs(self.request.user)
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
        context['available_verbs'] = self.object.get_available_verbs(self.request.user)
        return context

    def get_success_url(self):
        post = cm.get_media_post(self.object)
        action.send(self.request.user, verb='updated', action_object=self.object, target=post)
        return post.get_absolute_url()

    def get(self, request, *args, **kwargs):
        supes = super(MediaUpdateView, self).get(request, *args, **kwargs)
        context = self.get_context_data(**kwargs)
        if self.request.is_ajax():
            remote_form = RemoteForm(self.get_form(self.form_class))
            blob = {
                'form':remote_form.as_dict(),
                'available_verbs':self.object.get_available_verbs(self.request.user),
                'object_instance':None
            }
            data = json.dumps(blob)
            out_kwargs = {'content_type':'application/json'}
            return HttpResponse(data, **out_kwargs)

        return supes

#media ENDS