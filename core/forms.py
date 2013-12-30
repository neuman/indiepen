from django import forms
import core.models as cm


class ProjectForm(forms.ModelForm):
    class Meta:
        model = cm.Project
        fields = '__all__'

class PledgeForm(forms.ModelForm):
    class Meta:
        model = cm.Pledge
        exclude = ['person','token', 'project']

