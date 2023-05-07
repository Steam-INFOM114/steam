from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Task, Meeting, Resource
from django.utils.text import slugify
from django.contrib.auth import get_user_model


User = get_user_model()


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


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        exclude = ['project']
        labels = {
            'name': 'Nom',
            'description': 'Description',
            'file': 'Fichier',
            'is_hidden': 'Cachée'
        }
        widgets = {
            # TODO: localization of placeholders
            'name': forms.TextInput(attrs={'placeholder': 'Nom de la ressource'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description de la ressource', 'rows': 3})
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'  # ['name','description','start_date','end_date']
        labels = {
            'name': 'Nom',
            'description': 'Description',
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'status': 'Statut',
            'project': 'Projet'
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nom de la tâche', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description de la tâche', 'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-select'})
        }

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['name','description','start_date','project']
        labels = {
            'name': 'Nom',
            'description': 'Description',
            'start_date': 'Date de la réunion',
            'project': 'Projet'
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nom de la réunion', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description de la réunion', 'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
        }

class CustomUserCreationForm(UserCreationForm):

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return slugify(username)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + \
            ('first_name', 'last_name', 'email',)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].label = 'Nom d\'utilisateur'
            self.fields['username'].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.attrs['placeholder'] = 'Nom d\'utilisateur'
            self.fields['first_name'].label = 'Prénom'
            self.fields['first_name'].widget.attrs['class'] = 'form-control'
            self.fields['first_name'].widget.attrs['placeholder'] = 'Prénom'
            self.fields['last_name'].label = 'Nom'
            self.fields['last_name'].widget.attrs['class'] = 'form-control'
            self.fields['last_name'].widget.attrs['placeholder'] = 'Nom'
            self.fields['email'].label = 'Adresse email'
            self.fields['email'].widget.attrs['class'] = 'form-control'
            self.fields['email'].widget.attrs['placeholder'] = 'Adresse email'
            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].label = 'Mot de passe'
            self.fields['password1'].widget.attrs['placeholder'] = 'Mot de passe'
            self.fields['password2'].label = 'Confirmer le mot de passe'
            self.fields['password2'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirmer le mot de passe'
