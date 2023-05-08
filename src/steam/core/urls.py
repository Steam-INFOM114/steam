from django.urls import path
from .views import ProjectListView, ProjectDetailView, ProjectCreateView, ProjectRegisterView, ProjectUpdateView, ProjectDeleteView, ResourceListView, ResourceDetailView, ResourceCreateView, ResourceUpdateView, ResourceDeleteView, TaskDetail, TaskCreate, TaskUpdate, TaskList, TaskDeleteView, loginPage, logoutUser, registerPage


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
    path('project/<int:pk>/resources/',
         ResourceListView.as_view(), name='project-resource-list'),
    path('project/<int:pk>/resource/create/',
         ResourceCreateView.as_view(), name='resource-create'),
    path('resource/<int:pk>/', ResourceDetailView.as_view(), name='resource-detail'),
    path('resource/<int:pk>/update/',
         ResourceUpdateView.as_view(), name='resource-update'),
    path('resource/<int:pk>/delete/',
         ResourceDeleteView.as_view(), name='resource-delete'),
    path('project/register/', ProjectRegisterView.as_view(),
         name='project-register'),
    path('tasks/', TaskList.as_view(), name='task-list'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task/create/<int:project_id>', TaskCreate.as_view(), name='task-create'),
    path('task/<int:pk>/update/', TaskUpdate.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
]
