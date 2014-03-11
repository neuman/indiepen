from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

import core.views as cv
from core.remote_forms import my_ajax_view, handle_instance_form
from api import v1_api

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/posts/'), name='index'),
    url(r'bootstrap/$', cv.BootstrapView.as_view(), name='bootstrap'),
    ('^activity/', include('actstream.urls')),

    url(r'(?P<instance_model>\w+)/(?P<pk>\w+)/history/$', cv.HistoryListView.as_view(), name='history_list'),

    url(r'projects/$', cv.ProjectListView.as_view(), name='project_list'),
    url(r'projects/create/$', cv.ProjectCreateView.as_view(), name='project_create'),
    url(r'projects/(?P<pk>\d+)/$', cv.ProjectDetailView.as_view(), name='project_detail'),
    url(r'projects/(?P<pk>\d+)/pledge/$', cv.PledgeCreateView.as_view(), name='pledge_create'),
    url(r'projects/(?P<pk>\d+)/upload/$', cv.MediaCreateView.as_view(), name='media_create'),

    url(r'projects/(?P<pk>\d+)/pay/$', cv.PaymentMethodCreateView.as_view(), name='paymentmethod_create'),

    url(r'projects/(?P<pk>\d+)/post/$', cv.PostCreateView.as_view(), name='post_create'),
    url(r'posts/$', cv.PostListView.as_view(), name='post_list'),
    url(r'posts/(?P<pk>\d+)/$', cv.PostDetailView.as_view(), name='post_detail'),
    url(r'posts/(?P<pk>\d+)/upload/$', cv.PostMediaCreateView.as_view(), name='post_media_create'),
    url(r'posts/(?P<pk>\d+)/uploads/$', cv.PostUploadsView.as_view(), name='post_media_uploads'),
    url(r'posts/(?P<pk>\d+)/reorder/$', cv.PostReorderMediaView.as_view(), name='post_media_reorder'),

    url(r'medias/$', cv.MediaListView.as_view(), name='media_list'),
    url(r'medias/(?P<pk>\d+)/$', cv.MediaDetailView.as_view(), name='media_detail'),
    url(r'medias/(?P<pk>\d+)/history/$', cv.MediaHistoryView.as_view(), name='media_history'),
    url(r'medias/(?P<pk>\d+)/update/$', cv.MediaUpdateView.as_view(), name='media_update'),

    url(r'users/(?P<pk>\d+)/$', cv.UserDetailView.as_view(), name='user_detail'),
    url(r'users/create/$', cv.UserCreateView.as_view(), name='user_ceate'),
    url(r'users/login/$', cv.UserLoginView.as_view(), name='user_login'),
    url(r'users/logout/$', cv.UserLogoutView.as_view(), name='user_logout'),
    #(r'^users/login/$', 'django.contrib.auth.views.login',{'template_name': 'form.html'}),

    url(r'^(?P<pk>\d+)/$',cv.DetailView.as_view(), name="detail"),
    url(r'^api/', include(v1_api.urls)),
    url(r'^remoteform/$', my_ajax_view, name='remoteform'),
    url(r'^apps/(?P<app_label>\w+)/models/(?P<model_name>\w+)/instances/form/$', handle_instance_form, name='adminapi_handle_instance_add_form'),
    url(r'^apps/(?P<app_label>\w+)/models/(?P<model_name>\w+)/instances/(?P<pk>\d+)/form/$', handle_instance_form, name='adminapi_handle_instance_edit_form'),
)


