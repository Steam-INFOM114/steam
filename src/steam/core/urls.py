from django.urls import path
from . import viewGantt
from .views import MeetingCreate, MeetingUpdate, MeetingDeleteView, ProjectListView, ProjectDetailView, ProjectCreateView, ProjectRegisterView, ProjectUpdateView, ProjectDeleteView, TaskDetail, TaskCreate, TaskUpdate, TaskDeleteView, loginPage, logoutUser, registerPage


urlpatterns = [
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),
    path('register/', registerPage, name="register"),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('project/create/', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/update/',
         ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/delete/',
         ProjectDeleteView.as_view(), name='project-delete'),
    path('project/register/', ProjectRegisterView.as_view(), name='project-register'),
    path('tasks/', viewGantt.gantt, name='task-list'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task/create/', TaskCreate.as_view(), name='task-create'),
    path('task/createM/', MeetingCreate.as_view(), name='meeting-create'),
    path('task/<int:pk>/update/', TaskUpdate.as_view(), name='task-update'),
    path('task/<int:pk>/updateM/', MeetingUpdate.as_view(), name='meeting-update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('task/<int:pk>/deleteM/', MeetingDeleteView.as_view(), name='meeting-delete'),
]
