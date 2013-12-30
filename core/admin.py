from django.conf import settings
from django.contrib import admin
import core.models as core

admin.site.register(core.Person)
admin.site.register(core.Badge)
admin.site.register(core.Project)
admin.site.register(core.Post)
admin.site.register(core.Membership)
admin.site.register(core.Service)
admin.site.register(core.Media)
admin.site.register(core.Contribution)
admin.site.register(core.Payout)
admin.site.register(core.Pledge)