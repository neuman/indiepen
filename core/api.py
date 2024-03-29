# myapp/api.py
from tastypie.resources import ModelResource
import core.models as cm 
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authorization import Authorization

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

class ProjectResource(ModelResource):
    class Meta:
        queryset = cm.Project.objects.all()
        resource_name = 'project'
        excludes = ['ask']
        authorization = Authorization()
        list_allowed_methods = ['get', 'post', 'put']
        detail_allowed_methods = ['get']
        always_return_data = True

from tastypie.api import Api
v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ProjectResource())