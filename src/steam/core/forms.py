from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['owner']

        # TODO: localization of labels
        labels = {
            'name': 'Nom',
            'description': 'Description',
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'is_archived': 'Archivé',
            'members': 'Membres'
        }
        widgets = {
            # TODO: localization of placeholders
            'name': forms.TextInput(attrs={'placeholder': 'Nom du projet', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description du projet', 'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_archived': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
