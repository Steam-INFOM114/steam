from django.test import TestCase, Client
from django.urls import reverse
from core.models import Project,Task
from core.forms import TaskForm
from django.utils import timezone
from django.contrib.auth.models import User

class TaskUpdateTemplateTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(name='Créer une campagne publicitaire', description='Contacter des agences de publicité', start_date=timezone.now().date(),end_date=timezone.now().date() + timezone.timedelta(days=2), status='1')
        self.url = reverse('taskUpdate', args=[self.task.id])
        self.response = self.client.get(self.url)
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

    def test_update_task_template_form(self):
        """Test that the update_task.html template contains a form."""
        self.assertContains(self.response, '<form')  # Expect a form to be displayed

    def test_update_task_template_form_labels(self):
        """Test that the update_task.html template contains the correct form labels."""
        labels = self.response.content.decode().lower()
        self.assertIn('nom', labels)
        self.assertIn('description', labels)
        self.assertIn('date de début', labels)
        self.assertIn('date de fin', labels)
        self.assertIn('statut', labels)
        self.assertIn('projet', labels)

    def test_update_task_template_fields(self):
        """Test that the update task template contains all the input fields in the form."""
        response = self.client.get(self.url)
        self.assertContains(response, '<input', count=4)
        self.assertContains(response, 'name="name"', count=1)
        self.assertContains(response, 'name="description"', count=1)
        self.assertContains(response, 'name="start_date"', count=1)
        self.assertContains(response, 'name="end_date"', count=1)
        self.assertContains(response, 'name="status"', count=1)
        self.assertContains(response, 'name="project"', count=1)

    def test_update_task_template_invalid_date_format(self):
        """Test that the task update template displays an error message when the user enters an invalid date format"""
        invalid_data = self.valid_data.copy()
        invalid_data['start_date'] = '2022/03/15'
        invalid_data['end_date'] = '2022/03/16'
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid date.', count=2)

    def test_update_task_template_required_fields(self):
        """Test that the update task template shows error message for missing required fields."""
        invalid_data = {
            'name': '',
            'description': '',
            'start_date': '',
            'end_date': '',
            'status': '',
            'project': ''
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.', count=5)

