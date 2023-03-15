from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Project
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import ProjectForm, CustomUserCreationForm

class ProjectListView(ListView):
    model = Project
    template_name = 'project/list.html'
    context_object_name = 'projects'


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/create_update.html'
    success_url = reverse_lazy('project-list')

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/create_update.html'
    success_url = reverse_lazy('project-list')

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('project-list')


def loginPage(request):

    if request.user.is_authenticated:
        return redirect('project-list')

    if request.method == "POST": #get username and password
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try: #check if the user exists
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password) #make sure that the credentials are corrects and store user object based on username and password

        if user is not None and user.is_active:
            login(request,user) #log the user in create a session
            return redirect('project-list')
        else:
            messages.error(request, 'Username OR Password does not exists')

    return render(request, 'users/login.html')


def registerPage(request):

    form = UserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Log in the user
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('project-list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html',{'form':form})

def logoutUser(request):
    logout(request)
    return redirect('project-list')


