from django.conf.urls import patterns, include, url

import core.views as cv
from core.remote_forms import my_ajax_view, handle_instance_form
from api import v1_api

urlpatterns = patterns('',
    url(r'^$', cv.IndexView.as_view(), name='index'),
    url(r'bootstrap/$', cv.BootstrapView.as_view(), name='bootstrap'),
    url(r'projects/$', cv.ProjectsView.as_view(), name='projects'),
    url(r'projects/(?P<instance_id>\d+)/$', cv.ProjectView.as_view(), name='project'),
    url(r'projects/(?P<instance_id>\d+)/form/$', cv.PledgeFormView.as_view(), name='project_form'),
    url(r'projects/(?P<instance_id>\d+)/pledge/$', cv.PledgeCreate.as_view(), name='pledge_create'),
    url(r'projects/create/$', cv.ProjectCreate.as_view(), name='project_create'),
    url(r'^(?P<pk>\d+)/$',cv.DetailView.as_view(), name="detail"),
    url(r'^api/', include(v1_api.urls)),
    url(r'^remoteform/$', my_ajax_view, name='remoteform'),
    url(r'^apps/(?P<app_label>\w+)/models/(?P<model_name>\w+)/instances/form/$', handle_instance_form, name='adminapi_handle_instance_add_form'),
    url(r'^apps/(?P<app_label>\w+)/models/(?P<model_name>\w+)/instances/(?P<instance_id>\d+)/form/$', handle_instance_form, name='adminapi_handle_instance_edit_form'),
)


