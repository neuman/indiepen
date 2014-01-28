from django.db import models
import moneyed
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.urlresolvers import reverse
from carteblanche.models import Verb, Noun
#from simple_history.models import HistoricalRecords
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
import json



MEDIUM_CHOICES = (
    ('TXT', 'Text'),
    ('VID', 'Video'),
    ('AUD', 'Audio'),
    ('IMA', 'Image'),
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

FREQUENCY_CHOICES = (
    ('DAI', 'Daily'),
    ('WEE', 'Weekly'),
    ('MON', 'Monthly'),
)
FREQUENCIES = {
    "DAI":1,
    "WEE":7,
    "MON":30,
}

DURATION_CHOICES = (
    ('1', '1 Month'),
    ('2', '2 Months'),
    ('3', '3 Months'),
    ('4', '4 Months'),
    ('5', '5 Months'),
    ('6', '6 Months'),
)

IMPORTANCE_CHOICES = [(n, n) for n in xrange(1, 10, 1)]

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

    def get_touches(self):
        touches = []
        for a in self.history.all():
            t = Touch()
            t['title'] = self.__unicode__()
            t['updated_at'] = a.updated_at
            #t['url'] = a.get_absolute_url()
            t['action'] = "Updated"
            if a.changed_by_id != None:
                t['user'] = User.objects.get(id=a.changed_by_id)
            touches.append(t)

        return touches

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

class StreamListVerb(Verb):
    display_name = "View Stream"
    view_name='stream_list'
    required = True
    denied_message = "Sorry, you can't view that stream yet."

    def get_url(self):
        return reverse(viewname=self.view_name, kwargs={'instance_model':self.noun._meta.model_name, 'instance_id':self.noun.id}, current_app='core')

    def is_available(self, user):
        return self.noun.is_visible_to(user)

class Badge(Auditable):
    title = models.CharField(max_length=300)

    def __unicode__(self):
        return self.title

class ProjectCreateVerb(Verb):
    display_name = "Start New Project"
    view_name='project_create'
    required = False

    def get_url(self):
        return reverse(viewname=self.view_name, current_app='core')

class ProjectPledgeVerb(Verb):
    display_name = "Pledge"
    required = True
    denied_message = "Sorry, you already pledged!"
    view_name='pledge_create'
    
    def is_available(self, user):
        return Pledge.objects.filter(project=self.noun, pledger=user).count() == 0

    def get_url(self):
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app='core')

class ProjectMemberVerb(Verb):
    availability_key = "is_member"
    required = True 
    denied_message = "Sorry, you must be a member of the project to do this."

    def is_available(self, user):
        return self.noun.members.filter(id=user.id).count() > 0

class ProjectUploadVerb(ProjectMemberVerb):
    display_name = "Upload Media"
    view_name='media_create'
    required = True

    def get_url(self):
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app='core')

class ProjectPostVerb(ProjectMemberVerb):
    display_name = "Post"
    view_name='post_create'
    required = False

    def get_url(self):
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app='core')

class ProjectDetailVerb(ProjectMemberVerb):
    display_name = "View Project"
    view_name = 'project_detail'
    required = True
    denied_message = "Sorry, that project isn't published yet."

    def is_available(self, user):
        return self.noun.is_visible_to(user)

    def get_url(self):
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app='core')

class Project(Auditable, Noun):
    title = models.CharField(max_length=300)
    brief = models.TextField(default='')
    members = models.ManyToManyField(User)
    medium = models.CharField(max_length=3, choices=MEDIUM_CHOICES, default='TXT')
    duration = models.CharField(max_length=3, choices=DURATION_CHOICES, default='1')
    frequency = models.CharField(max_length=3, choices=FREQUENCY_CHOICES, default='WEE')
    #ask = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    ask = models.FloatField()
    upfront = models.FloatField()
    funded = models.BooleanField(default=False)
    #history = HistoricalRecords()
    verb_classes = [ProjectDetailVerb, ProjectPledgeVerb, ProjectUploadVerb, ProjectPostVerb, StreamListVerb]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(viewname='project_detail', args=[self.id], current_app='core')

    def is_visible_to(self, user):
        if self.noun.is_published():
            return True
        elif self.noun.members.filter(id=user.id).count() > 0:
                return True
        else:
            return False            

    def is_published(self):
        return self.get_posts().order_by('created_at')[0].is_published()

    def get_pledges(self):
        return Pledge.objects.filter(project=self)

    def get_days(self):
        return self.duration*FREQUENCIES['MON']

    def get_occurances_per_month(self):
        output = round(float(FREQUENCIES['MON'])/FREQUENCIES[self.frequency] )
        print(output)
        return int(output)

    def get_number_of_posts(self):
        output = int(self.duration)*self.get_occurances_per_month()
        return output

    def get_ask_per_post(self):
        count = self.get_number_of_posts()
        ask = float(self.ask-self.upfront)/count
        return ask

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
        output = (float(piece)/float(self.ask))*100
        print(output)
        return output

    def get_percent_pledged(self):
        output = self.get_percent(self.get_total_pledged())
        print(output)
        return output

    def get_percent_upfront(self):
        output = self.get_percent(self.upfront)
        print(output)
        return output

    def get_percent_per_post(self):
        output = self.get_percent(round((self.ask-self.upfront)/self.get_number_of_posts()))
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


from taggit.managers import TaggableManager
class MediaDetailVerb(Verb):
    display_name = "View Media"
    view_name = 'media_detail'
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
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app='core')

class MediaUpdateVerb(Verb):
    display_name = "Update Media Details"
    view_name='media_update'
    required = True

    def is_available(self, user):
        
        return self.noun.post_set.all()[0].project.members.filter(id=user.id).count() > 0

    def get_url(self):
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app='core')

class Media(Auditable, Noun):
    original_file = models.FileField(upload_to='/')
    internal_file = models.FileField(upload_to='/', null=True, blank=True)
    medium = models.CharField(max_length=3, choices=MEDIUM_CHOICES, null=True, blank=True)
    brief = models.TextField(default='', null=True, blank=True)
    tags = TaggableManager(blank=True)
    importance = models.IntegerField(default=5, choices=IMPORTANCE_CHOICES)
    #history = HistoricalRecords()
    verb_classes = [MediaDetailVerb, MediaUpdateVerb, StreamListVerb]

    noodles = {}

    def __unicode__(self):
        return self.get_file_name()

    def get_absolute_url(self):
        return reverse(viewname='media_detail', args=[self.id], current_app='core')

    def is_visible_to(self, user):
        post = get_media_post(self)
        if post.is_published():
            return True
        elif post.project.members.filter(id=user.id).count() > 0:
                return True
        else:
            return False

    def get_file_url(self):
        return self.original_file.url

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
                return self.original_file.name

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

def get_media_post(media):
    return media.post_set.all()[0]

class PostCreateMediaVerb(Verb):
    display_name = "Upload Post Files"
    view_name = 'post_media_uploads'
    required = True
    denied_message = "You must be a project member to upload to this post."

    def is_available(self, user):
        return self.noun.project.members.filter(id=user.id).count() > 0

    def get_url(self):
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app='core')


class PostDetailVerb(Verb):
    display_name = "View Post"
    view_name = 'post_detail'
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
        return reverse(viewname=self.view_name, args=[self.noun.id], current_app='core')


class Post(Auditable, Noun):
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=60)
    media = models.ManyToManyField(Media, null=True, blank=True)
    published = models.BooleanField(default=False)
    #history = HistoricalRecords()
    verb_classes = [PostDetailVerb,PostCreateMediaVerb,StreamListVerb]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(viewname='post_detail', args=[self.id], current_app='core')

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
        return self.media.all().order_by('-importance')

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


class Membership(Auditable):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    role = models.CharField(max_length=100)


class Service(Auditable, Noun):
    title = models.CharField(max_length=300)
    cost_per_hour = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    provider = models.ManyToManyField(User)
    #history = HistoricalRecords()

    def __unicode__(self):
        return self.title


class Pledge(Auditable, Noun):
    pledger = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    #value = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    value = models.FloatField()
    token = models.CharField(max_length=300)

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
    #history = HistoricalRecords()

class Payout(Auditable):
    payee = models.ForeignKey(User, null=True, blank=True)
    project = models.ForeignKey(Project, null=True, blank=True)
    value = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    #history = HistoricalRecords()

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

