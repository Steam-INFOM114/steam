from django import forms
from django.contrib.auth.models import User
from .models import Project

# TODO: use form in template
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        # TODO: localization of labels
        labels = {
            'name': 'Nom',
            'description': 'Description',
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'is_archived': 'Archivé',
            'owner': 'Propriétaire',
            'members': 'Membres'
        }
        widgets = {
            # TODO: localization of placeholders
            'name': forms.TextInput(attrs={'placeholder': 'Nom du projet', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description du projet', 'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_archived': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'owner': forms.Select(attrs={'class': 'form-select'}),
            # TODO: add widget with search option
            'members': forms.SelectMultiple(attrs={'class': 'form-select'})
        }
