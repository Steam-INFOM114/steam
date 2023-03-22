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

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        return (queryset.filter(members=user) | queryset.filter(owner=user)).distinct()


class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Project
    template_name = 'project/detail.html'
    context_object_name = 'project'

    def test_func(self):
        project = self.get_object()
        user = self.request.user
        return user == project.owner or user in project.members.all()


# TODO: authorization
class ProjectCreateView(LoginRequiredMixin, CreateView):
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
