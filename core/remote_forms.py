from django import forms
from django.core.serializers.json import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.middleware.csrf import CsrfViewMiddleware
from django.views.decorators.csrf import csrf_exempt

from django_remote_forms.forms import RemoteForm

from core.forms import ProjectForm

from django import forms

from django.utils.functional import Promise
#from django.utils.translation import force_unicode


class LazyEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Promise):
            return unicode(o)
        else:
            if callable(o):
                o = o()
            return super(LazyEncoder, self).default(o)

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


@csrf_exempt
def my_ajax_view(request):
    csrf_middleware = CsrfViewMiddleware()

    response_data = {}
    if request.method == 'GET':
        # Get form definition
        form = ProjectForm()


    elif request.raw_post_data:
        request.POST = json.loads(request.raw_post_data)
        # Process request for CSRF
        csrf_middleware.process_view(request, None, None, None)
        form_data = request.POST.get('data', {})
        form = ProjectForm(form_data)
        if form.is_valid():
            form.save()

    field_configuration = {
        'include': ['title','duration'],
    }

    remote_form = RemoteForm(form, **field_configuration)
    # Errors in response_data['non_field_errors'] and response_data['errors']
    response_data.update(remote_form.as_dict())

    response = HttpResponse(
        json.dumps(response_data, cls=DjangoJSONEncoder),
        mimetype="application/json"
    )

    # Process response for CSRF
    csrf_middleware.process_response(request, response)
    return response


from django.contrib.admin.sites import site
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.middleware.csrf import get_token, CsrfViewMiddleware
from django.utils.text import capfirst
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def handle_instance_form(request, app_label, model_name, instance_id=None):
    if not request.user.is_authenticated():
        return HttpResponse('Unauthorized', status=401)

    csrf_middleware = CsrfViewMiddleware()

    response_data = {
        'meta': {
            'app_label': app_label,
            'model_name': model_name
        },

        'admin': {}
    }

    instance = None

    for model, model_admin in site._registry.items():
        if app_label != model._meta.app_label or model_name != model._meta.module_name:
            continue

        field_configuration = {
            'include': model_admin.fields or [],
            'exclude': model_admin.exclude or [],
            'ordering': model_admin.fields or [],
            'fieldsets': model_admin.fieldsets or {},
            'readonly': model_admin.readonly_fields or []
        }

        if instance_id is not None:
            response_data[instance_id] = instance_id
            try:
                instance = model.objects.get(pk=instance_id)
            except model.DoesNotExist:
                raise Http404('Invalid instance ID')

        current_model = model

        CurrentModelForm = None

        if CurrentModelForm is None:
            class CurrentModelForm(forms.ModelForm):
                class Meta:
                    model = current_model

        if request.method == 'GET':
            # Return instance form for given model name
            # Return initial values if instance ID is supplied, otherwise return empty form
            if instance is None:
                form = CurrentModelForm()
            else:
                form = CurrentModelForm(instance=instance)
                for field_name, initial_value in form.initial.items():
                    if initial_value is not None and field_name in form.fields:
                        form.fields[field_name].initial = initial_value

            response_data['csrfmiddlewaretoken'] = get_token(request)

            remote_form = RemoteForm(form, **field_configuration)
            response_data.update(remote_form.as_dict())
        elif request.raw_post_data:
            request.POST = json.loads(request.raw_post_data)
            csrf_middleware.process_view(request, None, None, None)
            if 'data' in request.POST:
                if instance_id is None:
                    form = CurrentModelForm(request.POST['data'])
                else:
                    form = CurrentModelForm(request.POST['data'], instance=instance)
                if form.is_valid():
                    if not request.POST['meta']['validate']:
                        form.save()

                remote_form = RemoteForm(form, **field_configuration)
                response_data.update(remote_form.as_dict())

    response = HttpResponse(json.dumps(response_data, cls=LazyEncoder), mimetype="application/json")
    csrf_middleware.process_response(request, response)
    return response