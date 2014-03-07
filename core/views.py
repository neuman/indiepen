from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from uuid import uuid4

from carteblanche.base import Noun
#from carteblanche.django.mixins import NounView
from core.verbs import NounView

from api import v1_api
import core.models as cm
import core.forms as cf
import stripe

from django.db.models.signals import post_save
from actstream import action
from actstream.models import user_stream, action_object_stream, model_stream, actor_stream

from django.contrib.auth import authenticate, login

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from django.conf import settings

class SiteRootView(NounView):
    def get_noun(self, **kwargs):
        siteroot = cm.SiteRoot()
        return siteroot

class IndexView(SiteRootView, TemplateView):
    template_name = 'bootstrap.html'

class MessageView(SiteRootView, TemplateView):
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

class StreamListView(NounView, TemplateView):
    template_name = 'stream.html'

    def get_context_data(self, **kwargs):
        context = super(StreamListView, self).get_context_data(**kwargs)
        context['stream'] = self.noun.get_action_stream()
        return context

    def get_noun(self, **kwargs):
        object_type = ContentType.objects.get(app_label="core", model=self.kwargs['instance_model']).model_class()
        return get_object_or_404(object_type, pk=self.kwargs['pk'])

class ProjectView(NounView):
    def get_noun(self, **kwargs):
        return cm.Project.objects.get(id=self.kwargs['pk'])

class ProjectDetailView(ProjectView, TemplateView):
    template_name = 'project.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['project'] = self.noun
        context['total_pledged'] = self.noun.get_total_pledged()
        return context


class ProjectListView(SiteRootView, TemplateView):
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['projects'] = cm.Project.objects.all()
        return context

#Pledge STARTS
class PledgeCreateView(ProjectView, FormView):
    model = cm.Pledge
    template_name = 'form.html'
    fields = ['value']
    form_class = cf.PledgeForm
    success_message = "Thank you for pledging!"

    def get(self, request, **kwargs):
        #if the user has no payment methods, redirect to the view where one can be created
        if cm.get_user_payment_method(self.request.user) == None:
            return HttpResponseRedirect(cm.CreatePaymentMethodVerb(self.noun).get_url())
        else:
            return super(PledgeCreateView, self).get(request, **kwargs)

    def form_valid(self, form):
        form.instance.changed_by = self.request.user
        form.instance.pledger = self.request.user
        form.instance.project = cm.Project.objects.get(id=self.kwargs['pk'])
        self.object = form.save()
        return super(PledgeCreateView, self).form_valid(form)

    def get_success_url(self):
        action.send(self.request.user, verb='pledged', action_object=self.object, target=self.object.project)
        return cm.ProjectDetailVerb(self.noun).get_url()

    def dispatch(self, *args, **kwargs):
        self.noun = cm.Project.objects.get(id=self.kwargs['pk'])
        return super(PledgeCreateView, self).dispatch(*args, **kwargs)
#Pledge ENDS

#payment STARTS
class PaymentMethodCreateView(ProjectView, FormView):
    model = cm.PaymentMethod
    template_name = 'payment_form.html'
    form_class = cf.PaymentMethodForm
    fields = ['stripeToken']
    success_message = "Your new Payment Method was created successfully."

    def form_valid(self, form):
        # Create a Customer
        customer = stripe.Customer.create(
            api_key=settings.STRIPE_SECRET_KEY,
            card=form.cleaned_data['stripeToken'],
            description=self.request.user.email
        )
        # Save the customer ID in your database so you can use it later
        cm.PaymentMethod.objects.create(holder=self.request.user, customer_id=customer.id)
        #action.send(self.request.user, verb='pledged', action_object=self.object, target=self.object.project)
        return super(PaymentMethodCreateView, self).form_valid(form)

    def get_success_url(self):
        return cm.PledgeVerb(self.noun).get_url()

    def dispatch(self, *args, **kwargs):
        self.noun = cm.Project.objects.get(id=self.kwargs['pk'])
        return super(PaymentMethodCreateView, self).dispatch(*args, **kwargs)
#payment ENDS

class ProjectCreateView(SiteRootView, CreateView):
    model = cm.Project
    template_name = 'form.html'
    fields = '__all__'
    success_url = '/'
    form_class = cf.ProjectForm

    def get_success_url(self):
        self.object.members.add(self.request.user)
        action.send(self.request.user, verb='created', action_object=cm.get_history_most_recent(self.object), target=self.object)
        return reverse(viewname='project_detail', args=(self.object.id,), current_app='core')

class MediaCreateView(ProjectView, CreateView):
    model = cm.Media
    template_name = 'form.html'
    fields = '__all__'
    success_url = '/'

    def get_form(self, form_class):
        return cf.MediaForm(self.request.POST or None, self.request.FILES or None, initial=self.get_initial())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.changed_by = self.request.user
        action.send(self.request.user, verb='uploaded', action_object=cm.get_history_most_recent(self.object), target=self.object)
        return super(MediaCreateView, self).form_valid(form)


#Post STARTS
class PostView(NounView):
    def get_noun(self, **kwargs):
        return cm.Post.objects.get(id=self.kwargs['pk'])

class PostCreateView(ProjectView, CreateView):
    model = cm.Post
    template_name = 'form.html'
    success_url = '/'
    instance = None

    def get_form(self, form_class):
        return cf.PostForm(self.request.POST or None, self.request.FILES or None, initial=self.get_initial())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = cm.Project.objects.get(id=self.kwargs['pk'])
        form.instance.changed_by = self.request.user
        self.instance = form.instance
        return super(PostCreateView, self).form_valid(form)

    def get_success_url(self):
        action.send(self.request.user, verb='created', action_object=cm.get_history_most_recent(self.object), target=self.object)
        return reverse(viewname='post_media_uploads', args=(self.object.id,), current_app='core')

class PostUpdateView(PostView, UpdateView):
    model = cm.Post
    template_name = 'form.html'
    success_url = '/'

    def get_form(self, form_class):
        return cf.PostForm(self.request.POST or None, self.request.FILES or None, initial=self.get_initial())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = cm.Project.objects.get(id=self.kwargs['pk'])
        form.instance.changed_by = self.request.user
        return super(PostCreateView, self).form_valid(form)



import json

from django.http import HttpResponse
from django.views.generic.edit import CreateView

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.noun.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response



class PostReorderMediaView(PostView, FormView, AjaxableResponseMixin):
    model = cm.Post
    template_name = 'reorder.html'
    success_url = '/'

    def get_initial(self):
        '''
        set the field to have a list of media ids
        '''
        initial = super(PostReorderMediaView, self).get_initial()
        orderstring = str(self.noun.get_medias().values_list('id', flat=True))
        initial.__setitem__('orderstring', orderstring)
        return initial

    def get_form(self, form_class):
        return cf.MediaReorderForm(self.request.POST or None, self.request.FILES or None, instance=self.noun, initial=self.get_initial())

    def form_valid(self, form):
        orderstring = form.data['orderstring']
        orderstring_ids = form.parse_list_string(orderstring)
        for m in self.noun.get_medias():
            m.sort_order = orderstring_ids.index(m.id)
            m.save()
        return super(PostReorderMediaView, self).form_valid(form)

    def get_success_url(self):
        action.send(self.request.user, verb='reordered', action_object=cm.get_history_most_recent(self.noun), target=self.noun)
        return cm.PostDetailVerb(self.noun).get_url()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PostReorderMediaView, self).get_context_data(**kwargs)
        context['medias'] = self.noun.get_medias()
        return context

class PostDetailView(PostView, TemplateView):
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
        return cm.Post.objects.get(id=self.kwargs['pk'])

class PostListView(SiteRootView, TemplateView):
    template_name = 'posts.html'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['posts'] = cm.Post.objects.all().order_by('-updated_at')
        return context

class PostMediaCreateView(PostView, CreateView):
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
        p = cm.Post.objects.get(id=self.kwargs['pk'])
        p.media.add(self.new_instance)
        action.send(self.request.user, verb='uploaded', action_object=cm.get_history_most_recent(self.new_instance), target=self.object)
        return reverse(viewname='post_media_create', args=(self.kwargs['pk'],), current_app='core')

class PostUploadsView(PostView, TemplateView):
    template_name = 'uploads.html'

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(PostUploadsView, self).get_context_data(**kwargs)
        context['upload_url'] = reverse(viewname='post_media_create', args=(self.kwargs['pk'],), current_app='core')
        return context

#Post ENDS

#User STARTS 

class UserDetailView(TemplateView, Noun):
    template_name = 'user.html'

    def get_verbs(self):
        return [
            #cm.PostDetailVerb(cm.Post.objects.get(id=self.kwargs['pk']))
            ]

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['pk'])
        context['user'] = user
        context['available_verbs'] = None
        context['stream'] = actor_stream(user)
        return context

class UserCreateView(SiteRootView, CreateView):
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

class UserLoginView(SiteRootView, FormView):
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
class MediaDetailView(NounView, TemplateView):
    template_name = 'media.html'

    def get_context_data(self, **kwargs):
        context = super(MediaDetailView, self).get_context_data(**kwargs)
        media = self.noun
        context['medias'] = [media]
        context['available_verbs'] = media.get_available_verbs(self.request.user)
        context['focus'] = True
        return context

    def get_noun(self, **kwargs):
        return cm.Media.objects.get(id=self.kwargs['pk'])

class MediaHistoryView(NounView, TemplateView):
    template_name = 'media.html'

    def get_context_data(self, **kwargs):
        context = super(MediaHistoryView, self).get_context_data(**kwargs)
        media = self.noun
        context['medias'] = [media]
        context['available_verbs'] = media.get_available_verbs(self.request.user)
        context['focus'] = True
        return context

    def get_noun(self, **kwargs):
        history_instance = cm.HistoricalMedia.objects.get(id=self.kwargs['pk'])
        return cm.Media.objects.get(id=self.kwargs['pk'])

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
        action.send(self.request.user, verb='updated', action_object=cm.get_history_most_recent(self.object), target=self.object)
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