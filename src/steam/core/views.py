from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Project
from django.contrib.auth.models import User
from .forms import ProjectForm,TaskForm
from .models import Task

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

class TaskUpdate(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy('task-list')

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')
