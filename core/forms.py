from django import forms
import core.models as cm
from django.contrib.auth.models import User
import django.forms.extras.widgets as widgets


class BootstrapForm(forms.ModelForm):
    exclude = ['changed_by']
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs.has_key('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class':'form-control'})

class BooleanForm(forms.Form):
    decision = forms.BooleanField(required=True, label="Confirm", help_text="I swear, I'm ready to do this.")

    def clean(self):
        cleaned_data = super(BooleanForm, self).clean()
        decision = cleaned_data.get("decision")

        if decision==None:
            self._errors["decision"] = self.error_class(["You have to check the box if you want to publish."])
            # These fields are no longer valid. Remove them from the
            # cleaned data.


        # Always return the cleaned data, whether you have changed it or
        # not.
        return cleaned_data

class DropzoneForm(BootstrapForm):
    def __init__(self, *args, **kwargs):
        super(DropzoneForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs.has_key('class'):
                field.widget.attrs['class'] += ' form-control dropzone'
            else:
                field.widget.attrs.update({'class':'form-control dropzone'})

class ProjectForm(BootstrapForm):
    class Meta:
        model = cm.Project
        exclude = ['changed_by', 'members','funded', 'approved', 'first','ask_total','schedule']

class PostForm(BootstrapForm):
    class Meta:
        model = cm.Post
        exclude = ['changed_by', 'project', 'media','published']

class PledgeForm(BootstrapForm):
    class Meta:
        model = cm.Pledge
        fields = ['value']

class PaymentMethodForm(BootstrapForm):
    stripeToken = forms.CharField(max_length=300)
    class Meta:
        model = cm.PaymentMethod
        fields = ['stripeToken']

class MediaReorderForm(BootstrapForm):
    orderstring = forms.CharField(max_length=500)

    def get_media_ids(self):
        return self.instance.get_medias().values_list('id', flat=True)

    def parse_list_string(self, list_string):
        list_string = list_string.replace('[','').replace(']','').replace(' ','')
        try:
            list_string_ids = [int(n) for n in list_string.split(',')]
        except ValueError as e:
            raise forms.ValidationError("please use numeric ids only")
        return list_string_ids

    def clean_orderstring(self):
        orderstring = self.cleaned_data['orderstring']
        orderstring_ids = self.parse_list_string(orderstring)
        media_ids = self.get_media_ids()

        if len(orderstring_ids) != len(media_ids):
            raise forms.ValidationError("Please inpt "+str(len(media_ids))+" ids.")

        for o in orderstring_ids:
            if not o in media_ids:
                raise forms.ValidationError(str(o)+" is not one of this post's media's ids.")

        for o in media_ids:
            if not o in orderstring_ids:
                raise forms.ValidationError(str(o)+" wasn't included in your list of ids.")

        # Always return the cleaned data, whether you have changed it or
        # not.
        return self.cleaned_data['orderstring']

    class Meta:
        model = cm.Post
        fields = ['orderstring']

class MediaUpdateForm(BootstrapForm):
    class Meta:
        model = cm.Media
        exclude = ['internal_file','changed_by','medium', 'sort_order']

class MediaCreateForm(BootstrapForm):
    class Meta:
        model = cm.Media
        fields = ['original_file']


class RegistrationForm(BootstrapForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    # rest of the fields

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            self.add_error('password2', u"Didn't match first password..")
        return cleaned_data

    def save(self):
        return super(RegistrationForm, self).save()

    class Meta:
        model = User
        fields = ['email','first_name','last_name','password1','password1']

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _

class LoginForm(BootstrapForm):
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct %(email)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            temp_user = User.objects.get(email=email)
            self.user_cache = authenticate(username=temp_user.username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError('WARNING')
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

    class Meta:
     model = User
     fields = ['email','password']