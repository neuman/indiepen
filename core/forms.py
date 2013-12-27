from django import forms
import core.models as cm

# Create the form class.
class ProjectForm(forms.ModelForm):
    class Meta:
        model = cm.Project
        fields = '__all__'
