from django.db import models
import moneyed
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User

MEDIUM_CHOICES = (
    ('TXT', 'Text'),
    ('VID', 'Video'),
    ('AUD', 'Audio'),
    ('IMA', 'Image'),
    ('MUL', 'Multimedia'),
)

DURATION_CHOICES = (
    ('DAI', 'Daily'),
    ('WEE', 'Weekly'),
    ('MON', 'Monthly'),
)

class Badge(models.Model):
    title = models.CharField(max_length=300)

class Person(models.Model):
    user = models.OneToOneField(User)
    badges = models.ManyToManyField(Badge)

class Project(models.Model):
    title = models.CharField(max_length=300)
    members = models.ManyToManyField(Person)
    medium = models.CharField(max_length=3, choices=MEDIUM_CHOICES, default='TXT')
    duration = models.CharField(max_length=3, choices=MEDIUM_CHOICES, default='WEE')
    ask = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')

class Post(models.Model):
    title = models.CharField(max_length=60)
    members = models.ManyToManyField(Person, through='Membership')

class Membership(models.Model):
    person = models.ForeignKey(Person)
    post = models.ForeignKey(Post)
    role = models.CharField(max_length=100)

class Media(models.Model):
    original_file = models.FileField(upload_to='/')
    internal_file = models.FileField(upload_to='/')
    medium = models.CharField(max_length=3, choices=MEDIUM_CHOICES, default='TXT')


class Service(models.Model):
    title = models.CharField(max_length=300)
    cost_per_hour = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    prividing_Person = models.ManyToManyField(Person)


class Pledge(models.Model):
    person = models.ManyToManyField(Person)
    project = models.ManyToManyField(Project)
    ammount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    token = title = models.CharField(max_length=300)

class Contribution(models.Model):
    person = models.ManyToManyField(Person)
    pledge = models.ManyToManyField(Pledge)
    project = models.ManyToManyField(Project)
    ammount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')

class Payout(models.Model):
    person = models.ManyToManyField(Person)
    project = models.ManyToManyField(Project)
    ammount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')