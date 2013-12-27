from django.conf.urls import patterns, include, url

from .views import IndexView, DetailView, BootstrapView
from .remote_forms import my_ajax_view, handle_instance_form
from api import v1_api

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'bootstrap/$', BootstrapView.as_view(), name='bootstrap'),
    url(r'^(?P<pk>\d+)/$',DetailView.as_view(), name="detail"),
    url(r'^api/', include(v1_api.urls)),
    url(r'^remoteform/$', my_ajax_view, name='remoteform'),
    url(r'^apps/(?P<app_label>\w+)/models/(?P<model_name>\w+)/instances/form/$', handle_instance_form, name='adminapi_handle_instance_add_form'),
    url(r'^apps/(?P<app_label>\w+)/models/(?P<model_name>\w+)/instances/(?P<instance_id>\d+)/form/$', handle_instance_form, name='adminapi_handle_instance_edit_form'),
)


