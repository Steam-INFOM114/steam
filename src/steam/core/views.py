from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Project, Task, Meeting
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from .forms import ProjectForm, TaskForm, CustomUserCreationForm, MeetingForm
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class ProjectListView(ListView):
    model = Project
    template_name = 'project/list.html'
    context_object_name = 'projects'

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/create_update.html'
    success_url = reverse_lazy('project-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        context['users'] = User.objects.exclude(pk=self.request.user.pk)
        return context


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/create_update.html'
    success_url = reverse_lazy('project-list')

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        context['users'] = User.objects.exclude(pk=self.request.user.pk)
        return context

class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('project-list')

class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = "tasks/task.html"

class TaskCreate(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy('task-list')

class TaskUpdate(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy('task-list')

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')

class MeetingCreate(CreateView):
    model = Meeting
    form_class = MeetingForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy('task-list')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('project-list')
    if request.method == "POST":  # get username and password
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        # Check if the user exists
        try:
            user_exists = User.objects.get(username=username)
        except User.DoesNotExist:
            user_exists = None
        if user_exists:
            # Make sure that the credentials are corrects and store user object based on username and password
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('project-list')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'User does not exist.')
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

    return render(request, 'users/register.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('project-list')
