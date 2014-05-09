from django.db import models
import moneyed
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.urlresolvers import reverse
from carteblanche.base import Verb, Noun
#from carteblanche.django.mixins import DjangoVerb
from core.verbs import DjangoVerb, availability_login_required
from simple_history.models import HistoricalRecords
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
import json
from django.contrib.contenttypes.models import ContentType
import actstream
from django.db.models import Q
import uuid
import os
from core.verbs import *



PROJECT_PHASE_CHOICES = (
    ('PRI', 'Private'),
    ('DEL', 'Deliberation'),
    ('OPE', 'Open'),
    ('FUN', 'Funded'),
    ('CAN', 'Canceled'),
    ('COM', 'Completed'),
)

IMPORTANCE_CHOICES = (
    ('low', 'Small'),
    ('med', 'Medium'),
    ('hig', 'Large')
)

def get_file_path(instance, filename):
    blocks = filename.split('.')
    ext = blocks[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    instance.name = blocks[0]
    return os.path.join('uploads/', filename)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    thumbnail_url = models.CharField(max_length=400)

    def get_facebook_id(self):
        if self.thumbnail_url == '':
            self.thumbnail_url = self.user.social_auth.all()[0].uid
            self.save()
        return self.thumbnail_url

    def get_projects(self):
        self.user.project_set.all()

    def get_visible_posts(self, user):
        return Post.objects.filter(project__members=self.user)



User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

@python_2_unicode_compatible
class Auditable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    changed_by = models.ForeignKey(User, null=True, blank=True, related_name="%(app_label)s_%(class)s_related")

    def __str__(self):
        return "auditable string goes here"

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user_setter(self, value):
        self.changed_by = value

    def get_action_stream(self):
        stream = actstream.models.Action.objects.filter(self.get_action_stream_query()).order_by('-timestamp')
        return stream

    def get_action_stream_query(self):
        post_type = ContentType.objects.get_for_model(self)
        query = Q(target_object_id=self.id, target_content_type=post_type)
        return query

    def get_class_name(self):
        return self.__class__.__name__

    class Meta:
        abstract = True

MEDIUM_CHOICES = (
    ('TXT', 'Text'),
    ('VID', 'Video'),
    ('AUD', 'Audio'),
    ('IMG', 'Image'),
    ('MUL', 'Multimedia'),
    ('DAT', 'Data'),
)

FREQUENCY_CHOICES = (
    ('DAI', 'Daily'),
    ('WEE', 'Weekly'),
    ('MON', 'Monthly'),
)

DURATION_CHOICES = (
    ('1', '1 Month'),
    ('2', '2 Months'),
    ('3', '3 Months'),
    ('4', '4 Months'),
    ('5', '5 Months'),
    ('6', '6 Months'),
)



class Badge(Auditable):
    title = models.CharField(max_length=300)

    def __unicode__(self):
        return self.title

class Project(Auditable, Noun):
    title = models.CharField(max_length=300, help_text="examples: Why Do Men Bite Dogs?")
    brief = models.TextField(default='', help_text="A short complete description of exactly what you will do.  If for any reason you do not follow through on this, you will not be paid, so think about it carefully.")
    schedule = models.TextField(default='', help_text="examples: Daily, Every Other Tuesday, Single Post")
    planned_posts = models.PositiveIntegerField(help_text="How many posts do you intend to produce?")
    end_date = models.DateField(help_text="This is when the project will close fully, all unused money is returned to the pledgers. Must be within the next 6 months. Please use the following format: <em>YYYY-MM-DD</em>.")
    ask_total = models.FloatField(default=0)
    ask_per_post = models.FloatField(help_text="How much it will cost to get each post made.  This can include expenses for living, travel, accomodations, per diems, etc.")
    upfront_ask = models.FloatField(help_text="Here you can ask for the crowd to cover any upfront expenses you have.  Please include a detailed breakdown in the project brief. examples: plane tickets, equipment")
    #phase = models.CharField(max_length=3, choices=PROJECT_PHASE_CHOICES, null=True, blank=True)
    first = models.ForeignKey('Post', related_name="%(app_label)s_%(class)s_related", null=True, blank=True)
    upfront_ask = models.FloatField(help_text="Here you can ask for the crowd to cover any upfront expenses you have.  examples: plane tickets, equipment")
    members = models.ManyToManyField(User)
    history = HistoricalRecords()
    verb_classes = [ProjectDetailVerb, CreatePledgeVerb, CreatePaymentMethodVerb, ProjectPostVerb, HistoryListVerb]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(viewname='project_detail', args=[self.id], current_app=APPNAME)

    def is_visible_to(self, user):
        if self.is_published():
            return True
        elif self.members.filter(id=user.id).count() > 0:
                return True
        else:
            return False            

    def is_published(self):
        try:
            return self.get_posts().order_by('created_at')[0].is_published()
        except Exception as e:
            return False

    def can_pledge(self, user):
        return Pledge.objects.filter(project=self, pledger=user).count() == 0

    def get_pledges(self):
        return Pledge.objects.filter(project=self)

    def get_number_of_posts(self):
        return self.planned_posts

    def get_ask_total(self):
        return self.upfront_ask+(self.ask_per_post * self.planned_posts)

    def get_ask_per_post(self):
        return self.ask_per_post

    def get_asks_per_post(self):
        return [self.get_ask_per_post()]*self.get_number_of_posts()

    def get_total_pledged(self):
        sums = Pledge.objects.filter(project=self).aggregate(Sum('value'))
        if sums['value__sum'] == None:
            total = 0
        else:
            total = sums['value__sum']
        return total

    def get_percent(self, piece):
        output = (float(piece)/float(self.get_ask_total()))*100
        print(output)
        return output

    def get_percent_pledged(self):
        output = self.get_percent(self.get_total_pledged())
        print(output)
        return output

    def get_percent_upfront(self):
        output = self.get_percent(self.upfront_ask)
        print(output)
        return output

    def get_number_of_posts(self):
        return self.planned_posts

    def get_percent_per_post(self):
        output = self.get_percent(round((self.ask_per_post)))
        print(output)
        return output

    def get_members(self):
        return self.members.all()

    def get_posts(self):
        return Post.objects.filter(project=self)

    def get_thumb_url(self):
        q = Post.objects.filter(project=self)
        if q.count() > 0:
            return q[0].get_thumb_url()
        else:
            return None

    def get_action_stream_query(self):
        self_type = ContentType.objects.get_for_model(self)
        query = Q(target_object_id=self.id, target_content_type=self_type)
        for p in self.get_posts():
            query = query | p.get_action_stream_query()
        return query


from taggit.managers import TaggableManager
import logging
logger = logging.getLogger(__name__)

MEDIA_TYPE_CHOICES = (
    ('V', 'Video'),
    ('A', 'Audio'),
    ('I', 'Image'),
    ('D', 'Document'),
    ('U', 'Unknown')
)

MEDIUM_CHOICES = (
    ('TXT', 'Text'),
    ('VID', 'Video'),
    ('AUD', 'Audio'),
    ('IMG', 'Image'),
    ('MUL', 'Multimedia'),
    ('DAT', 'Data'),
)

EXTENSIONS = {
    "TXT":['txt','md'],
    "VID":['avi', 'm4v', 'mov', 'mp4', 'mpeg', 'mpg', 'vob', 'wmv'],
    "AUD":['aac', 'aiff', 'm4a', 'mp3', 'wav', 'wma'],
    "IMA":['gif', 'jpeg', 'jpg', 'png'],
    "MUL":[],
    "DAT":['csv','json'],
}

CONVERSION_STATUS = (
    ('U', 'Unconverted'),
    ('Q', 'In Conversion Queue'),
    ('I', 'In Progress'),
    ('C', 'Converted'),
    ('E', 'Error'),
)

VIDEO_EXTENSIONS = [
    'avi',
    'm4v',
    'mov',
    'mp4',
    'mpeg',
    'mpg',
    'vob',
    'wmv',
    'mkv',
]
AUDIO_EXTENSIONS = [
    'aac',
    'aiff',
    'm4a',
    'mp3',
    'wav',
    'wma',
]
IMAGE_EXTENSIONS = [
    'gif',
    'jpeg',
    'jpg',
    'png',
]
DOCUMENT_EXTENSIONS = [
    'doc',
    'docx',
    'mus',
    'pdf',
    'ppt',
    'pptx',
    'rtf',
    'sib',
    'txt',
    'xls',
    'xlsx',
]
ALL_EXTS = VIDEO_EXTENSIONS + AUDIO_EXTENSIONS + IMAGE_EXTENSIONS +\
    DOCUMENT_EXTENSIONS

class Media(Auditable, Noun):
    original_file = models.FileField(upload_to=get_file_path, null=True, blank=True)
    internal_file = models.FileField(upload_to='/', null=True, blank=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    medium = models.CharField(max_length=3, choices=MEDIUM_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=1, choices=CONVERSION_STATUS, null=True, blank=True)
    brief = models.TextField(default='', null=True, blank=True)
    tags = TaggableManager(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    importance = models.CharField(max_length=3, choices=IMPORTANCE_CHOICES, default='med')
    history = HistoricalRecords()
    verb_classes = [MediaDetailVerb, MediaUpdateVerb, HistoryListVerb, MediaPostDetailVerb]

    noodles = {}

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(viewname='media_detail', args=[self.id], current_app=APPNAME)

    def is_visible_to(self, user):
        post = get_media_post(self)
        if post.is_published():
            return True
        elif post.project.members.filter(id=user.id).count() > 0:
                return True
        else:
            return False

    def get_file_url(self):
        try:
            return self.internal_file.url
        except ValueError:
            return None

    def set_internal_file_s3_key(self, key):
        self.internal_file.name = key
        self.save()

    def get_original_s3_key(self):
        return self.original_file.name.lstrip('/')

    def get_content(self):
        return self.original_file._get_file().read()
        #avoid pulling from s3 constantly
        if not self.noodles.__contains__('content'):
            self.noodles.__setitem__('content',self.original_file._get_file().read())
        return self.noodles['content']

    def get_content_data_values(self):
        content = self.get_content()
        content = json.loads(content)

        try:
            value_name = content['y_name']
        except Exception as e:
            value_name = 'value'
        output = [point[value_name] for point in content['data']]
        return output

    def get_content_data_labels(self):
        content = self.get_content()
        content = json.loads(content)
        try:
            label_name = content['x_name']
        except Exception as e:
            label_name = 'label'
        output = [point[label_name] for point in content['data']]
        return output

    def get_file_name(self):
        return self.name

    def get_file_extension(self):
        #return string_in.__getslice__(string_in.__len__()-3, string_in.__len__()).lower()
        i = self.get_file_url().rfind(".")
        return string_in.__getslice__(i+1, string_in.__len__()).lower()

    def get_medium(self):
        for medium in cm.EXTENSIONS:
            for extension in cm.EXTENSIONS[medium]:
                if extension == self.get_file_extension():
                    return medium

    def is_file_nonzero(self):
        if self.file.size > 0:
                    return True
        return False

    def get_post(self):
        return get_media_post(self)

    #for celery
    @property
    def noext(self):
        return os.path.splitext(self.s3_key)[0]

    @property
    def basename(self):
        return os.path.splitext(os.path.basename(self.s3_key))[0]

    @property
    def fileext(self):
        return os.path.splitext(self.s3_key)[1][1:]

    def reprocess(self):
        self.update(set__status='U', set__s3_key=self.original_s3_key)
        from ddesk.tasks import get_info
        get_info.apply_async(args=[str(self.id)])

    def set_complete(self):
        self.status = 'C'
        self.save()
        #get applications
        for application in self.get_applications():
            app_media = application.get_medias_proxy()
            if app_media.count() == app_media.filter(status='C').count():
                application.update(set__in_progress=False)
                # Immediate notifications have been suppressed until now since
                # media was being converted, so update all reviewers that
                # have immediate update frequency
                application.notify_reviewers()

def get_media_post(media):
    return media.post_set.all()[0]

def get_user_payment_method(user):
    q = PaymentMethod.objects.filter(holder=user).order_by('created_at')
    if q.count() > 0:
        return q[0]
    else:
        return None

class Post(Auditable, Noun):
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=60)
    media = models.ManyToManyField(Media, null=True, blank=True)
    submitted = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    history = HistoricalRecords()
    verb_classes = [PostDetailVerb,PostCreateMediaVerb,HistoryListVerb, PostCreateMediasVerb, PostReorderMediasVerb, PostSubmitVerb, PostProjectDetailVerb]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(viewname='post_detail', args=[self.id], current_app=APPNAME)

    def is_published(self):
        return self.published

    def is_visible_to(self, user):
        if self.is_published():
            return True
        elif self.project.members.filter(id=user.id).count() > 0:
                return True
        else:
            return False

    def get_medias(self):
        return self.media.all().order_by('sort_order','created_at')

    def get_summary_medias(self):
        return self.get_medias()[:2]

    def get_thumb(self):
        q = self.get_medias().filter(medium='IMG')
        if q.count() > 0:
            return q[0]
        else:
            return None

    def get_thumb_url(self):
        t = self.get_thumb()
        if t != None:
            return t.get_file_url()
        else:
            return None

    def get_action_stream_query(self):
        self_type = ContentType.objects.get_for_model(self)
        query = Q(target_object_id=self.id, target_content_type=self_type)
        for m in self.get_medias():
            query = query | m.get_action_stream_query()
        return query
        


class Membership(Auditable):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    role = models.CharField(max_length=100)


class Service(Auditable, Noun):
    title = models.CharField(max_length=300)
    cost_per_hour = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    provider = models.ManyToManyField(User)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.title

class PaymentMethod(Auditable):
    holder = models.ForeignKey(User)
    customer_id = models.CharField(max_length=300)

    def __unicode__(self):
        return self.customer_id

class Pledge(Auditable, Noun):
    pledger = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    #value = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    value = models.FloatField()
    payment_method = models.ForeignKey(PaymentMethod, null=True, blank=True)

    def __unicode__(self):
        return "$"+str(self.value)
'''
    class Meta(Auditable.Meta):
        __name__ = "ROOSTER"
        verbose_name = _('pledge')
        verbose_name_plural = _('pledges')
        swappable = 'CORE_PLEDGE_MODEL'
'''


class Contribution(Auditable):
    contributer = models.ManyToManyField(User)
    pledge = models.ManyToManyField(Pledge)
    project = models.ManyToManyField(Project)
    value = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    history = HistoricalRecords()

class Payout(Auditable):
    payee = models.ForeignKey(User, null=True, blank=True)
    project = models.ForeignKey(Project, null=True, blank=True)
    value = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    history = HistoricalRecords()

class Touch(dict):

    _keys = ['title','brief','url','updated_at','user','action']

    def __init__(self):
        for key in self._keys:
            self[key] = None

    def populateDict(self):
        self['B'] = 10
        self['A'] = 12


class Options(models.Model):
    user = models.ForeignKey(User, unique=True)
    image = models.FileField(null=True, blank=True, upload_to='/')

    def get_image_url(self):
        return self.image.url



def sort_touches(touches):
    return sorted(touches, key = lambda t: t['updated_at'], reverse=True)

def super_search(model, fields, matches, strings, initial=None):
    """
    Designed to lesson the code needed to run complex searches with ORed filters.
    Model: the model being queried.
    fields: an iterable containing string names of fields to query.
    match:  an iterable containing strings of what type of Django lookup to apply to those fields.
    strings: an iterable containing strings to be matched.
    """
    queries = []
    for field in fields:
        for string in strings:
            for match in matches:
                kwargs = {'%s__%s' % (field, match): string}
                queries.append(Q(**kwargs))
    #if there are no filters return no objects
    if queries.__len__() < 1:
        return model.objects.none()
    q = queries[0]
    for query in queries:
        q = q | query
    if initial != None:
        return initial.filter(q)
    else:
        return model.objects.filter(q)

def get_history_most_recent(instance):
    return instance.history.all().order_by('-updated_at')[0]



