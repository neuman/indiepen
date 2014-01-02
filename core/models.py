from django.db import models
import moneyed
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.urlresolvers import reverse
from actions.models import Action, Actionable


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

class Badge(models.Model):
    title = models.CharField(max_length=300)

    def __unicode__(self):
        return self.title

class Person(models.Model):
    user = models.OneToOneField(User)
    badges = models.ManyToManyField(Badge, null=True, blank=True)

    def __unicode__(self):
        return self.user.email


class ProjectPledgeAction(Action):
    display_name = "Pledge"
    def is_available(self, person):
        if self.instance.members.filter(id=person.id).count() > 0:
            return True
        else:
            return False

    def get_url(self):
        return reverse(viewname='pledge_create', args=[self.instance.id], current_app='core')

class ProjectCreateAction(Action):
    display_name = "Start New Project"

    def get_url(self):
        return reverse(viewname='project_create', current_app='core')

class Project(models.Model, Actionable):
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
        return reverse(viewname='project', args=[self.id], current_app='core')

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

    def get_actions(self):
        actions = [
            ProjectPledgeAction(instance=self)
        ]
        return actions

class Post(models.Model):
    title = models.CharField(max_length=60)
    members = models.ManyToManyField(Person, through='Membership')

class Membership(models.Model):
    person = models.ForeignKey(Person)
    post = models.ForeignKey(Post)
    role = models.CharField(max_length=100)

class Media(models.Model):
    original_file = models.FileField(upload_to='/')
    internal_file = models.FileField(upload_to='/', null=True, blank=True)
    medium = models.CharField(max_length=3, choices=MEDIUM_CHOICES, default='TXT', null=True, blank=True)


class Service(models.Model):
    title = models.CharField(max_length=300)
    cost_per_hour = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    prividing_Person = models.ManyToManyField(Person)


class Pledge(models.Model):
    person = models.ForeignKey(Person)
    project = models.ForeignKey(Project)
    ammount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    token = models.CharField(max_length=300)

class Contribution(models.Model):
    person = models.ManyToManyField(Person)
    pledge = models.ManyToManyField(Pledge)
    project = models.ManyToManyField(Project)
    ammount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')

class Payout(models.Model):
    person = models.ForeignKey(Person)
    project = models.ForeignKey(Project)
    ammount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')