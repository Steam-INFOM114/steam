from django.urls import path
from .views import ProjectCreateView, ProjectUpdateView

urlpatterns = [
    path('project/create/', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/update/',
         ProjectUpdateView.as_view(), name='project-update'),
]
