from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Project
from .forms import ProjectForm


class ProjectListView(ListView):
    model = Project
    template_name = 'project/list.html'
    context_object_name = 'projects'


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/create_update.html'
    success_url = reverse_lazy('project-list')


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/create_update.html'
    success_url = reverse_lazy('project-list')


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('project-list')
