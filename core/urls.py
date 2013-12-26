from django.conf.urls import patterns, include, url

from .views import IndexView, DetailView
from api import v1_api

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$',DetailView.as_view(), name="detail"),
    (r'^api/', include(v1_api.urls)),
)


