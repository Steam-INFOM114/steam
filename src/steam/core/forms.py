from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Task
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()

# TODO: use form in template


class ProjectForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'start_date',
            'end_date',
            'is_archived',
            'owner',
            'members'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        # self.fields['members'].queryset = User.objects.all().exclude(id=self.instance.owner.id)
        self.fields['members'].queryset = User.objects.all()


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True,
    )

    class Meta:
        model = Task
        fields = '__all__'  # ['name','description','start_date','end_date']
        labels = {
            'name': 'Nom',
            'description': 'Description',
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'status': 'Statut',
            'project': 'Projet',
            'assignees': 'Assignés',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nom de la tâche', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description de la tâche', 'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        p_id = kwargs.pop('project_id', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        # Set the project value
        if not p_id: # if project_id is not passed as argument, then it is an update so we get the project id from the instance
            p_id = self.instance.project.id
        project = Project.objects.get(id=p_id)
        self.fields['project'].initial = project  # set the initial value of project field to project object
        self.fields['project'].disabled = True

        # Add assignees values. Only the members of the project and the owner can be assignees
        self.fields['assignees'].queryset =  User.objects.filter(
            Q(projects__id=p_id) | Q(owned_projects=p_id))

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
