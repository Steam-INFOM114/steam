from django.urls import path
from . import views
from . import viewGantt
from .views import ProjectListView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView, TaskDetail,TaskCreate, TaskUpdate

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
    #path('tasks/',TaskList.as_view(),name='tasks'), #TESTING
    path('tasks/',viewGantt.gantt,name='task-list'),
    path('tasks/task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('tasks/create/',TaskCreate.as_view(),name='task-create'),
    path('tasks/update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('tasks/delete/<int:id>', views.delete, name='task-delete'),
]
