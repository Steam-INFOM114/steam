from django.test import TestCase, Client
from django.urls import reverse
from core.models import Project,Task
from core.forms import TaskForm
from django.utils import timezone
from django.contrib.auth.models import User

class TaskUpdateViewTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(name='Créer une campagne publicitaire', description='Contacter des agences de publicité', start_date=timezone.now().date(),end_date=timezone.now().date() + timezone.timedelta(days=2), status='1')
        self.url = reverse('taskUpdate', args=[self.task.id])
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.project = Project.objects.create(
            name="Project1",
            description="...",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=8),
            is_archived=False,
            owner=self.user
        )
        self.valid_data = {
            'name': 'Créer une campagne publicitaire',
            'description': 'Contacter des agences de publicité',
            'start_date': timezone.now().date(),
            'end_date': timezone.now().date() + timezone.timedelta(days=5),
            'status': '2',
            'project': self.project.pk
        }

    def test_task_update_view_get(self):
        """Test that the update task view renders the correct template and form for GET requests."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_form.html')

    def test_task_update_view_updates_task(self):
        """Test that the update task is updated in db"""
        response = self.client.post(self.url, data=self.valid_data)
        self.task.refresh_from_db()
        self.assertEqual(self.task.end_date, self.valid_data['end_date'])
        self.assertEqual(self.task.status, self.valid_data['status'])

    def test_update_task_with_valid_data(self):
        """Test that submitting a valid form redirects to the list of tasks"""
        response = self.client.post(self.url, data=self.valid_data)
        self.assertRedirects(response, reverse('tasks'))

    def test_update_task_view_end_date_before_start_date(self):
        """Test that the update task view doesn't create a new task with an end_date before start_date"""
        invalid_data = self.valid_data.copy()
        invalid_data['start_date'] = timezone.now().date() + timezone.timedelta(days=7)
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        # Expect the task object to have the original data
        updated_task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(updated_task.name, self.task.name)
        self.assertEqual(updated_task.description, self.task.description)
        self.assertEqual(updated_task.start_date, self.task.start_date)
        self.assertEqual(updated_task.end_date, self.task.end_date)
        self.assertEqual(updated_task.status, self.task.status)

    def test_update_task_view_invalid_status_choice(self):
            """Test that the update task view doesn't update an existing task with an invalid status choice."""
            invalid_data = self.valid_data.copy()
            invalid_data['status'] = '4'
            response = self.client.post(self.url, data=invalid_data)
            self.assertEqual(response.status_code, 200)
            # Expect the task object to have the original data
            updated_task = Task.objects.get(pk=self.task.pk)
            self.assertEqual(updated_task.name, self.task.name)
            self.assertEqual(updated_task.description, self.task.description)
            self.assertEqual(updated_task.start_date, self.task.start_date)
            self.assertEqual(updated_task.end_date, self.task.end_date)
            self.assertEqual(updated_task.status, self.task.status)

    def test_update_task_with_empty_data(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)
