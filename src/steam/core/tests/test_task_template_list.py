from django.test import TestCase
from core.models import Project,Task
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class TasksListTemplateTest(TestCase):
    def setUp(self):
        self.url = reverse('task-list')
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.project = Project.objects.create(
            name="testproject",
            description="this is a test project",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            is_archived=False,
            owner=self.user
        )

    def test_list_tasks_template_success(self):
        """Test that the list tasks template shows tasks and contains delete confirmation modals"""
        # Create some tasks
        self.task1 = Task.objects.create(name='Task 1', description='Description 1', start_date='2022-03-15', end_date='2022-03-16', project=self.project)
        self.task2 = Task.objects.create(name='Task 2', description='Description 2', start_date='2022-03-15', end_date='2022-03-16', project=self.project)
        self.task3 = Task.objects.create(name='Task 3', description='Description 3', start_date='2022-03-15', end_date='2022-03-16', project=self.project)
        # Make a GET request to the list view
        response = self.client.get(self.url)
        # Verify that the response contains the expected tasks
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)
        self.assertContains(response, self.task3.name)
        self.assertContains(response, 'Êtes-vous sûr de vouloir supprimer la tâche')
        self.assertContains(response, 'Confirmer')
        self.assertContains(response, 'Annuler')

    def test_list_tasks_template_empty(self):
        """Test that the list tasks template shows a message when there are no tasks"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aucune tâche trouvée")
