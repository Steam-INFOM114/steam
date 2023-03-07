from django.urls import path
from .views import ProjectListView, ProjectCreateView, ProjectUpdateView

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('project/create/', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/update/',
         ProjectUpdateView.as_view(), name='project-update'),
]
