from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Task, Resource
from .forms import ProjectForm, TaskForm, CustomUserCreationForm, ResourceForm
from django.http import JsonResponse


User = get_user_model()


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project/list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_staff:
            return queryset

        return (queryset.filter(members=user) | queryset.filter(owner=user)).distinct()


class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Project
    template_name = 'project/detail.html'
    context_object_name = 'project'

    def test_func(self):
        project = self.get_object()
        user = self.request.user
        return user == project.owner or \
               user in project.members.all() or \
               user.is_staff

class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/create_update.html'
    success_url = reverse_lazy('project-list')

    def test_func(self):
        return self.request.user.is_staff

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

    def test_func(self):
        project = self.get_object()
        user = self.request.user
        return user == project.owner or \
               user.is_staff


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('project-list')

    def test_func(self):
        project = self.get_object()
        user = self.request.user
        return user == project.owner or \
               user.is_staff

class ProjectRegisterView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # get the project key from the form data
        key = request.POST.get('key')
        try:
            # try to get the project with the provided key
            project = Project.objects.get(key=key)
        except Project.DoesNotExist:
            # if the project doesn't exist, show an error message
            messages.error(request, 'Le projet avec la clé fournie n\'existe pas.', extra_tags='danger')
            return redirect('project-list')
        else:
            if request.user in project.members.all() or request.user == project.owner:
                messages.info(request, f'Vous êtes déjà inscrit au projet: {project.name}.')
            else:
                # add the user to the project
                project.members.add(request.user)
                messages.success(request, f'Vous êtes désormais inscrit au projet: {project.name}.')
                # TODO: rediriger vers la page gantt du projet
            return redirect('project-list')

    def get(self, request, *args, **kwargs):
        return JsonResponse({'error': 'GET method not allowed'}, status=405)


class ResourceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Resource
    template_name = 'resource/resource_list.html'
    context_object_name = 'resources'

    def get_queryset(self):
        user = self.request.user
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        queryset = super().get_queryset()

        is_staff = user.is_staff
        is_owner = user == project.owner
        is_member = user in project.members.all()

        if is_staff or is_owner:
            queryset_filtered = queryset.filter(project=project)
        elif is_member:
            queryset_filtered = queryset.filter(
                project=project, is_hidden=False)
        else:
            queryset_filtered = queryset.none()

        return queryset_filtered

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        context['pk'] = self.kwargs['pk']
        context['project'] = project
        return context

    def test_func(self):
        user = self.request.user
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        is_staff = user.is_staff
        is_owner = user == project.owner
        is_member = user in project.members.all()
        return is_staff or is_owner or is_member


class ResourceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Resource
    template_name = 'resource/resource_detail.html'
    context_object_name = 'resource'

    def test_func(self):
        user = self.request.user
        resource = self.get_object()
        project = resource.project
        is_staff = user.is_staff
        is_owner = user == project.owner
        is_member = user in project.members.all()

        return (is_member and not resource.is_hidden) or is_staff or is_owner


class ResourceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Resource
    form_class = ResourceForm
    template_name = "resource/resource_form.html"

    def form_valid(self, form):
        form.instance.project_id = self.kwargs['pk']
        return super().form_valid(form)

    def test_func(self):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        user = self.request.user
        return user == project.owner or \
            user.is_staff

    def get_success_url(self):
        return reverse_lazy('project-resource-list', kwargs={'pk': self.kwargs['pk']})


class ResourceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'resource/resource_form.html'

    def test_func(self):
        resource = self.get_object()
        project = resource.project
        user = self.request.user
        return user == project.owner or \
            user.is_staff

    def get_success_url(self):
        resource = self.get_object()
        project_id = resource.project.id
        return reverse_lazy('project-resource-list', kwargs={'pk': project_id})


class ResourceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Resource

    def test_func(self):
        resource = self.get_object()
        project = resource.project
        user = self.request.user
        return user == project.owner or \
            user.is_staff

    def get_success_url(self):
        resource = self.get_object()
        project_id = resource.project.id
        return reverse_lazy('project-resource-list', kwargs={'pk': project_id})


class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = "tasks/task.html"


class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = "tasks/tasks.html"


class TaskCreate(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy('task-list')

    def get_form_kwargs(self):
        kwargs = super(TaskCreate, self).get_form_kwargs()
        kwargs['project_id'] = self.kwargs['project_id']  # add project_id to form kwargs
        return kwargs

    # If project id is not in db,raise 404 error
    def dispatch(self, request, *args, **kwargs):
        try:
            self.project = Project.objects.get(id=self.kwargs['project_id'])
        except Project.DoesNotExist:
            raise Http404('Project does not exist')
        return super(TaskCreate, self).dispatch(request, *args, **kwargs)

class TaskUpdate(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy('task-list')


class TaskDeleteView(DeleteView):
    model = Task
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
