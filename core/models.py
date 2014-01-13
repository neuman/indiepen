from django.db import models
import moneyed
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.urlresolvers import reverse
from actions.models import Action, Actionable
from simple_history.models import HistoricalRecords


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

class Auditable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    changed_by = models.ForeignKey('Person', null=True, blank=True, related_name="%(app_label)s_%(class)s_related")

    '''
    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user_setter(self, value):
        self.changed_by = value
    '''

    class Meta:
        abstract = True

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

class Badge(Auditable):
    title = models.CharField(max_length=300)

    def __unicode__(self):
        return self.title

class Person(Auditable):
    user = models.OneToOneField(User)
    badges = models.ManyToManyField(Badge, null=True, blank=True)

    def __unicode__(self):
        return self.user.email

class ProjectCreateAction(Action):
    display_name = "Start New Project"

    def get_url(self):
        return reverse(viewname='project_create', current_app='core')

class ProjectPledgeAction(Action):
    display_name = "Pledge"
    def is_available(self, person):
        return self.instance.members.filter(id=person.id).count() > 0

    def get_url(self):
        return reverse(viewname='pledge_create', args=[self.instance.id], current_app='core')

class ProjectUploadAction(Action):
    display_name = "Upload Media"
    def is_available(self, person):
        return self.instance.members.filter(id=person.id).count()

    def get_url(self):
        return reverse(viewname='media_create', args=[self.instance.id], current_app='core')

class ProjectPostAction(Action):
    display_name = "Post"
    def is_available(self, person):
        return self.instance.members.filter(id=person.id).count() > 0

    def get_url(self):
        return reverse(viewname='post_create', args=[self.instance.id], current_app='core')

class ProjectAction(Action):
    display_name = "Upload Media"
    def is_available(self, person):
        return self.instance.members.filter(id=person.id).count()

    def get_url(self):
        return reverse(viewname='media_create', args=[self.instance.id], current_app='core')

class Project(Auditable, Actionable):
    title = models.CharField(max_length=300)
    brief = models.TextField(default='')
    members = models.ManyToManyField(Person)
    medium = models.CharField(max_length=3, choices=MEDIUM_CHOICES, default='TXT')
    duration = models.CharField(max_length=3, choices=DURATION_CHOICES, default='1')
    frequency = models.CharField(max_length=3, choices=FREQUENCY_CHOICES, default='WEE')
    ask = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(viewname='project_detail', args=[self.id], current_app='core')

    def get_pledges(self):
        return Pledge.objects.filter(project=self)

    def get_total_pledged(self):
        sums = Pledge.objects.filter(project=self).aggregate(Sum('ammount'))
        if sums['ammount__sum'] == None:
            total = 0
        else:
            total = sums['ammount__sum']
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


class Media(Auditable):
    original_file = models.FileField(upload_to='/')
    internal_file = models.FileField(upload_to='/', null=True, blank=True)
    medium = models.CharField(max_length=3, choices=MEDIUM_CHOICES, null=True, blank=True)
    brief = models.TextField(default='')
    tags = TaggableManager()

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

    def is_available(self, person):
        return self.instance.project.members.filter(id=person.id).count()

    def get_url(self):
        return reverse(viewname='post_media_uploads', args=[self.instance.id], current_app='core')

class PostDetailAction(Action):
    display_name = "View Post"

    def get_url(self):
        return reverse(viewname='post_detail', args=[self.instance.id], current_app='core')

class Post(Auditable, Actionable):
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=60)
    #members = models.ManyToManyField(Person)
    media = models.ManyToManyField(Media, null=True, blank=True)
    history = HistoricalRecords()

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
        q = self.get_media().filter(medium='IMA')
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
    person = models.ForeignKey(Person)
    post = models.ForeignKey(Post)
    role = models.CharField(max_length=100)

class Service(Auditable):
    title = models.CharField(max_length=300)
    cost_per_hour = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    prividing_Person = models.ManyToManyField(Person)


class Pledge(Auditable):
    person = models.ForeignKey(Person)
    project = models.ForeignKey(Project)
    ammount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    token = models.CharField(max_length=300)

class Contribution(Auditable):
    person = models.ManyToManyField(Person)
    pledge = models.ManyToManyField(Pledge)
    project = models.ManyToManyField(Project)
    ammount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')

class Payout(Auditable):
    person = models.ForeignKey(Person, null=True, blank=True)
    project = models.ForeignKey(Project, null=True, blank=True)
    ammount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')