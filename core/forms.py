from django import forms
import core.models as cm

# Create the form class.
class ProjectForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    class Meta:
        model = cm.Project
        fields = '__all__'
