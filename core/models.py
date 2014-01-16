from django.db import models
import moneyed
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.urlresolvers import reverse
from actions.models import Action, Actionable
#from simple_history.models import HistoricalRecords
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _



MEDIUM_CHOICES = (
    ('TXT', 'Text'),
    ('VID', 'Video'),
    ('AUD', 'Audio'),
    ('IMA', 'Image'),
    ('MUL', 'Multimedia'),
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

EXTENSIONS = {
    "TXT":['txt','md'],
    "VID":['avi', 'm4v', 'mov', 'mp4', 'mpeg', 'mpg', 'vob', 'wmv'],
    "AUD":['aac', 'aiff', 'm4a', 'mp3', 'wav', 'wma'],
    "IMA":['gif', 'jpeg', 'jpg', 'png'],
    "MUL":['csv','json'],
}

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

class ProjectCreateAction(Action):
    display_name = "Start New Project"

    def get_url(self):
        return reverse(viewname='project_create', current_app='core')

class ProjectPledgeAction(Action):
    display_name = "Pledge"
    def is_available(self, user):
        return self.instance.members.filter(id=user.id).count() > 0

    def get_url(self):
        return reverse(viewname='pledge_create', args=[self.instance.id], current_app='core')

class ProjectUploadAction(Action):
    display_name = "Upload Media"
    def is_available(self, user):
        return self.instance.members.filter(id=user.id).count()

    def get_url(self):
        return reverse(viewname='media_create', args=[self.instance.id], current_app='core')

class ProjectPostAction(Action):
    display_name = "Post"
    def is_available(self, user):
        return self.instance.members.filter(id=user.id).count() > 0

    def get_url(self):
        return reverse(viewname='post_create', args=[self.instance.id], current_app='core')

class ProjectAction(Action):
    display_name = "Upload Media"
    def is_available(self, user):
        return self.instance.members.filter(id=user.id).count()

    def get_url(self):
        return reverse(viewname='media_create', args=[self.instance.id], current_app='core')

class Project(Auditable, Actionable):
    title = models.CharField(max_length=300)
    brief = models.TextField(default='')
    members = models.ManyToManyField(User)
    medium = models.CharField(max_length=3, choices=MEDIUM_CHOICES, default='TXT')
    duration = models.CharField(max_length=3, choices=DURATION_CHOICES, default='1')
    frequency = models.CharField(max_length=3, choices=FREQUENCY_CHOICES, default='WEE')
    #ask = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    ask = models.FloatField()
    #history = HistoricalRecords()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(viewname='project_detail', args=[self.id], current_app='core')

    def get_pledges(self):
        return Pledge.objects.filter(project=self)

    def get_total_pledged(self):
        sums = Pledge.objects.filter(project=self).aggregate(Sum('value'))
        if sums['value__sum'] == None:
            total = 0
        else:
            total = sums['value__sum']
        return total

    def get_percent_pledged(self):
        return (float(self.get_total_pledged())/float(self.ask))*100

    def get_members(self):
        return self.members.all()

    def get_posts(self):
        return Post.objects.filter(project=self)

    def get_actions(self):
        actions = [
            ProjectPledgeAction(instance=self),
            ProjectUploadAction(instance=self),
            ProjectPostAction(instance=self)
        ]
        return actions

    def get_thumb_url(self):
        q = Post.objects.filter(project=self)
        if q.count() > 0:
            return q[0].get_thumb_url()
        else:
            return None


from taggit.managers import TaggableManager


class Media(Auditable, Actionable):
    original_file = models.FileField(upload_to='/')
    internal_file = models.FileField(upload_to='/', null=True, blank=True)
    medium = models.CharField(max_length=3, choices=MEDIUM_CHOICES, null=True, blank=True)
    brief = models.TextField(default='')
    tags = TaggableManager()
    #history = HistoricalRecords()

    def __unicode__(self):
        return self.get_file_name()

    def get_file_url(self):
        return self.original_file.url

    def get_content(self):
        return self.original_file._get_file().read()

    def get_file_name(self):
                return self.original_file.name

    def is_file_nonzero(self):
        if self.file.size > 0:
                    return True
        return False

class PostCreateMediaAction(Action):
    display_name = "Upload Post Files"

    def is_available(self, user):
        return self.instance.project.members.filter(id=user.id).count()

    def get_url(self):
        return reverse(viewname='post_media_uploads', args=[self.instance.id], current_app='core')

class PostDetailAction(Action):
    display_name = "View Post"

    def get_url(self):
        return reverse(viewname='post_detail', args=[self.instance.id], current_app='core')

class Post(Auditable, Actionable):
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=60)
    media = models.ManyToManyField(Media, null=True, blank=True)
    #history = HistoricalRecords()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(viewname='post_detail', args=[self.id], current_app='core')

    def get_actions(self):
        actions = [
            PostCreateMediaAction(instance=self)
        ]
        return actions

    def get_media(self):
        return self.media.all()

    def get_thumb(self):
        q = self.get_media().filter(medium='IMG')
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

    def get_audit(self):
        touches = self.get_touches()
        for m in self.media.all():
            touches+=m.get_touches()
            print m
        touches = sorted(touches, key = lambda t: t['updated_at'], reverse=True)
        return touches


class Membership(Auditable):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    role = models.CharField(max_length=100)


class Service(Auditable, Actionable):
    title = models.CharField(max_length=300)
    cost_per_hour = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    provider = models.ManyToManyField(User)
    #history = HistoricalRecords()

    def __unicode__(self):
        return self.title


class Pledge(Auditable, Actionable):
    pledger = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    #value = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    value = models.FloatField()
    token = models.CharField(max_length=300)

    def __unicode__(self):
        return self.pledger.__unicode__()+" + "+self.project.__unicode__()
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

    def get_touches(self):
        touches = []
        touchables = [pledge.objects.filter(pledger=self.user), self.user.project_set.all()]

    def get_audit(self):
        touches = self.get_touches()
        for m in self.media.all():
            touches+=m.get_touches()
            print m
        touches = sort_touches(touches)
        return touches


def sort_touches(touches):
    return sorted(touches, key = lambda t: t['updated_at'], reverse=True)