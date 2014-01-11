from django import forms
import core.models as cm


class BootstrapForm(forms.ModelForm):
    exclude = ['changed_by']
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs.has_key('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class':'form-control'})

class ProjectForm(BootstrapForm):
    class Meta:
        model = cm.Project
        exclude = ['changed_by', 'members']

class PostForm(BootstrapForm):
    class Meta:
        model = cm.Post
        exclude = ['changed_by', 'project', 'media']

class PledgeForm(BootstrapForm):
    class Meta:
        model = cm.Pledge
        fields = ['ammount']

class MediaForm(BootstrapForm):
    class Meta:
        model = cm.Media
        fields = '__all__'

class MediaCreateForm(BootstrapForm):
    class Meta:
        model = cm.Media
        fields = ['original_file']

