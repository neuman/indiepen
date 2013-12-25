from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import core.api as ca
from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(ca.UserResource())
v1_api.register(ca.PersonResource())
v1_api.register(ca.ProjectResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'indiepen.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls)),
)
