import carteblanche.base as cb
from django.views.generic import DetailView
from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve
from django.template import RequestContext
from django.core.urlresolvers import reverse
from functools import wraps
from django.utils.decorators import available_attrs
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

class NounView(SuccessMessageMixin):
    success_message = "That worked!"

    def __init__(self, **kwargs):
        super(NounView, self).__init__(**kwargs)
        self.noun = None
        
    def get_view_required_verbs(self, view_name):
        verbs = []
        for v in self.noun.get_verbs():
            if v.required == True:
                if v.view_name == view_name:
                    verbs.append(v)
        return verbs

    def get_view_required_unavailable_verbs(self, view_name, user):
        verbs = []
        for v in self.get_view_required_verbs(view_name):
            if not v.is_available(user):
                verbs.append(v)
        return verbs

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NounView, self).get_context_data(**kwargs)
        available_verbs = self.noun.get_available_verbs(self.request.user)
        context['available_verbs'] = available_verbs
        context['conditions'] = self.noun.conditions.get_available(self.request.user)
        self.noun.conditions.cache = {}
        return context

    def dispatch(self, *args, **kwargs):
        self.noun = self.get_noun(**kwargs)
        #what verbs are required and available for viewing of this page
        #for each of those, get a forbidden message and direct the user to a messaging view
        view_name = resolve(self.request.path_info).url_name
        denied_messages = []
        for verb in self.get_view_required_unavailable_verbs(view_name, self.request.user):
            denied_messages.append(verb.denied_message)
        if len(denied_messages) > 0:
            for message in denied_messages:
                messages.add_message(self.request, messages.ERROR, message)
            return render_to_response('messages.html',{"available_verbs":self.noun.get_available_verbs(self.request.user)}, RequestContext(self.request))
        
        return super(NounView, self).dispatch(*args, **kwargs)

    class Meta:
        abstract = True

class DjangoVerb(cb.Verb):
    view_name = None
    app = None
    visible = True

    def get_url(self):
        '''
        Default django get_url for urls that require no args.
        '''
        return reverse(viewname=self.view_name, current_app=self.app)

def availability_login_required(is_available_func):
    @wraps(is_available_func, assigned=available_attrs(is_available_func))
    def decorator(self, user):
        print user
        if user.is_authenticated(): 
            return is_available_func(self, user)
        else:
            self.denied_message = "You must be logged in to "+self.display_name+"."
            return False
    return decorator


from carteblanche.base import Verb, Noun
APPNAME = 'core'

class CoreVerb(DjangoVerb):
    app = APPNAME
    condition_name = 'public'

class UnauthenticatedOnlyVerb(CoreVerb):
    condition_name = 'is_unauthenticated'
    required = True

    def is_available(self, user):
        #only available to non-logged in users
        if user.is_authenticated():
            return False
        return True

class StreamListVerb(CoreVerb):
    display_name = "View Stream"
    view_name='stream_list'
    required = True
    denied_message = "Sorry, you can't view that stream yet."

    def get_url(self):
        return reverse(viewname=self.view_name, kwargs={'instance_model':self.noun._meta.model_name, 'instance_id':self.noun.id}, current_app=self.app)

    def is_available(self, user):
        return self.noun.is_visible_to(user)

class ProjectCreateVerb(CoreVerb):
    display_name = "Start New Project"
    view_name='project_create'
    condition_name = 'is_authenticated'
    required = True


    @availability_login_required
    def is_available(self, user):
        return True


class SiteJoinVerb(UnauthenticatedOnlyVerb):
    display_name = "Join Indiepen"
    view_name='user_ceate'

class SiteLoginVerb(UnauthenticatedOnlyVerb):
    display_name = "Login"
    view_name='user_login'


class SiteRoot(Noun):
    '''
    A hack that lets pages that have no actual noun have verbs and verb-based permissions. 
    '''
    verb_classes = [ProjectCreateVerb, SiteJoinVerb, SiteLoginVerb]

    class Meta:
        abstract = True

class PledgeVerb(CoreVerb):
    denied_message = "Sorry, you already pledged!"
    view_name='pledge_create'

    @availability_login_required
    def is_available(self, user):
        return Pledge.objects.filter(project=self.noun, pledger=user).count() == 0

    def get_url(self):
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app=self.app)

class CreatePledgeVerb(PledgeVerb):
    display_name = "Pledge"
    view_name='pledge_create'

class CreatePaymentMethodVerb(PledgeVerb):
    display_name = "Add New Payment Method"
    view_name='paymentmethod_create'
    visible = False

class ProjectVerb(DjangoVerb):
    def get_url(self):
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app=self.app)

class ProjectMemberVerb(ProjectVerb):
    condition_name = "is_member"
    required = True
    denied_message = "Sorry, you must be a member of the project to do this."

    @availability_login_required
    def is_available(self, user):
        return self.noun.members.filter(id=user.id).count() > 0

class ProjectPostVerb(ProjectMemberVerb):
    display_name = "Post"
    view_name='post_create'

class ProjectDetailVerb(ProjectVerb):
    display_name = "View Project"
    view_name = 'project_detail'
    condition_name = "can_view"
    required = True
    denied_message = "Sorry, that project isn't published yet."

    def is_available(self, user):
        return self.noun.is_visible_to(user)

class MediaDetailVerb(DjangoVerb):
    display_name = "View Media"
    view_name = 'media_detail'
    condition_name = 'can_view'
    required = True
    denied_message = "Sorry, that media isn't published yet."

    def is_available(self, user):
        post = get_media_post(self.noun)
        if post.is_published():
            return True
        elif post.project.members.filter(id=user.id).count() > 0:
                return True
        else:
            return False

    def get_url(self):
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app=self.app)

class MediaUpdateVerb(CoreVerb):
    display_name = "Update Media Details"
    view_name='media_update'
    required = True

    @availability_login_required
    def is_available(self, user):
        return self.noun.post_set.all()[0].project.members.filter(id=user.id).count() > 0

    def get_url(self):
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app=self.app)


class PostMemberVerb(CoreVerb):
    denied_message = "You must be a project member to upload to this post."
    condition_name = "is_member"

    @availability_login_required
    def is_available(self, user):
        return self.noun.project.members.filter(id=user.id).count() > 0

    def get_url(self):
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app=self.app)

class PostCreateMediasVerb(PostMemberVerb):
    display_name = "Upload Post Files"
    view_name = 'post_media_uploads'

class PostCreateMediaVerb(PostMemberVerb):
    display_name = "Upload a File"
    view_name = 'post_media_create'
    visible = False


class PostDetailVerb(CoreVerb):
    display_name = "View Post"
    view_name = 'post_detail'
    condition_name = "can_view"
    required = True
    denied_message = "Sorry, that post isn't published yet."

    def is_available(self, user):
        if self.noun.is_published():
            return True
        elif self.noun.project.members.filter(id=user.id).count() > 0:
                return True
        else:
            return False

    def get_url(self):
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app=self.app)

