from django import forms
from .models import OngoingProject, ProjectComponentStatus
from django.forms import inlineformset_factory

class OngoingProjectForm(forms.ModelForm):
    class Meta:
        model = OngoingProject
        exclude = ['status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

ProjectComponentStatusFormSet = inlineformset_factory(
    OngoingProject,
    ProjectComponentStatus,
    fields=['component', 'material_procurement', 'fabrication', 'hdg', 'powder_coating', 'erection'],
    extra=3,  # For 3 components: 3m, 5m, Gate
    can_delete=False
)
