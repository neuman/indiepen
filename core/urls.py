from django.conf.urls import patterns, include, url

import core.views as cv
from core.remote_forms import my_ajax_view, handle_instance_form
from api import v1_api

urlpatterns = patterns('',
    url(r'^$', cv.IndexView.as_view(), name='index'),
    url(r'bootstrap/$', cv.BootstrapView.as_view(), name='bootstrap'),
    ('^activity/', include('actstream.urls')),

    url(r'(?P<instance_model>\w+)/(?P<instance_id>\w+)/stream/$', cv.StreamListView.as_view(), name='stream_list'),

    url(r'projects/$', cv.ProjectListView.as_view(), name='project_list'),
    url(r'projects/create/$', cv.ProjectCreateView.as_view(), name='project_create'),
    url(r'projects/(?P<instance_id>\d+)/$', cv.ProjectDetailView.as_view(), name='project_detail'),
    url(r'projects/(?P<instance_id>\d+)/pledge/$', cv.PledgeCreateView.as_view(), name='pledge_create'),
    url(r'projects/(?P<instance_id>\d+)/upload/$', cv.MediaCreateView.as_view(), name='media_create'),

    url(r'projects/(?P<instance_id>\d+)/post/$', cv.PostCreateView.as_view(), name='post_create'),
    url(r'projects/(?P<instance_id>\d+)/posts/$', cv.PostListView.as_view(), name='post_list'),
    url(r'posts/(?P<instance_id>\d+)/$', cv.PostDetailView.as_view(), name='post_detail'),
    url(r'posts/(?P<instance_id>\d+)/upload/$', cv.PostMediaCreateView.as_view(), name='post_media_create'),
    url(r'posts/(?P<instance_id>\d+)/uploads/$', cv.PostUploadsView.as_view(), name='post_media_uploads'),

    url(r'medias/(?P<instance_id>\d+)/$', cv.MediaDetailView.as_view(), name='media_detail'),
    url(r'medias/(?P<pk>\d+)/update/$', cv.MediaUpdateView.as_view(), name='media_update'),

    url(r'users/(?P<instance_id>\d+)/$', cv.UserDetailView.as_view(), name='user_detail'),

    url(r'^(?P<pk>\d+)/$',cv.DetailView.as_view(), name="detail"),
    url(r'^api/', include(v1_api.urls)),
    url(r'^remoteform/$', my_ajax_view, name='remoteform'),
    url(r'^apps/(?P<app_label>\w+)/models/(?P<model_name>\w+)/instances/form/$', handle_instance_form, name='adminapi_handle_instance_add_form'),
    url(r'^apps/(?P<app_label>\w+)/models/(?P<model_name>\w+)/instances/(?P<instance_id>\d+)/form/$', handle_instance_form, name='adminapi_handle_instance_edit_form'),
)


