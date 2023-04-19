from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Task, Meeting
from django.utils.text import slugify
from django.contrib.auth import get_user_model


User = get_user_model()

# TODO: use form in template


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

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        # self.fields['members'].queryset = User.objects.all().exclude(id=self.instance.owner.id)
        self.fields['members'].queryset = User.objects.all()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__' #['name','description','start_date','end_date']
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
    first_name = forms.CharField(
        max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(
        max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True,
                             help_text='Required. Enter a valid email address.')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return slugify(username)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + \
            ('first_name', 'last_name', 'email',)
