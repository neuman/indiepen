from django import forms
import core.models as cm


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs.has_key('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class':'form-control'})
    class Meta:
        model = cm.Project
        fields = '__all__'

class PledgeForm(forms.ModelForm):
    class Meta:
        model = cm.Pledge
        exclude = ['person','token', 'project']

