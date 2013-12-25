# myapp/api.py
from tastypie.resources import ModelResource
import core.models as cm 
from django.contrib.auth.models import User
from tastypie import fields

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

class PersonResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = cm.Person.objects.all()
        resource_name = 'person'

class ProjectResource(ModelResource):
    class Meta:
        queryset = cm.Project.objects.all()
        resource_name = 'project'
        excludes = ['ask']