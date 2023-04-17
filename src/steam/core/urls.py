from django.urls import path
from .views import ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView, TaskDetail, TaskCreate, TaskUpdate, TaskList, TaskDeleteView, loginPage, logoutUser, registerPage


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
    path('tasks/', TaskList.as_view(), name='task-list'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task/create/', TaskCreate.as_view(), name='task-create'),
    path('task/<int:pk>/update/', TaskUpdate.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
]
