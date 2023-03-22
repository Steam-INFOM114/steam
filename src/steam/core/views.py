from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy,reverse
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

class TaskCreate(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy('tasks')

class TaskUpdate(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy('tasks')

def delete(request, id):
  task = Task.objects.get(id=id)
  task.delete()
  return HttpResponseRedirect(reverse('tasks'))
