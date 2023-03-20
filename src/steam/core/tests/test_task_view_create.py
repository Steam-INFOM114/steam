from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Project, Task
from django.utils import timezone


class TaskCreateViewTest(TestCase):
    def setUp(self):
        self.url = reverse('taskCreate')
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
        self.valid_data = {
            'name': 'Test task',
            'description': 'This is a test task.',
            'start_date': timezone.now().date(),
            'end_date': timezone.now().date() + timezone.timedelta(days=1),
            'status': '1',
            'project': self.project.pk
        }

    def test_create_task_view_get(self):
        """Test that the create task view renders the correct template and form for GET requests."""
        response = self.client.get(self.url)
        # Expect a successful GET request
        self.assertEqual(response.status_code, 200)
        # Expect the correct template to be used
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        form = response.context['form']
        self.assertIsInstance(form, TaskForm)

    def test_create_task_view_success(self):
        """Test that the create task view creates a new task with valid data."""
        response = self.client.post(self.url, data=self.valid_data)
        # Expect a redirect after successful form submission
        self.assertRedirects(response, reverse('tasks'))
        # Expect one task object to be created
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.name, self.valid_data['name'])
        self.assertEqual(task.description, self.valid_data['description'])
        self.assertEqual(task.start_date, self.valid_data['start_date'])
        self.assertEqual(task.end_date, self.valid_data['end_date'])
        self.assertEqual(task.status, self.valid_data['status'])
        self.assertEqual(task.project.pk, self.valid_data['project'])

    def test_create_task_view_empty_data(self):
        """Test that the create task view does not create a new task with empty data."""
        response = self.client.post(self.url, data={})
        # Expect the form to be re-rendered with errors
        self.assertEqual(response.status_code, 200)
        # Expect no task objects to be created
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_view_end_date_before_start_date(self):
        """Test that the create task view does not create a new task with an end_date before start_date"""
        invalid_data = self.valid_data.copy()
        invalid_data['start_date'] = timezone.now().date(
        ) + timezone.timedelta(days=2)  # end_date before start_date
        response = self.client.post(self.url, data=invalid_data)
        # Expect the form to be re-rendered with errors
        self.assertEqual(response.status_code, 200)
        # Expect no task objects to be created
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_view_invalid_status_choice(self):
        """Test that the create task view does not create a new task with an invalid status choice."""
        invalid_data = self.valid_data.copy()
        invalid_data['status'] = '4'  # Invalid choice
        response = self.client.post(self.url, data=invalid_data)
        # Expect the form to be re-rendered with errors
        self.assertEqual(response.status_code, 200)
        # Expect no task objects to be created
        self.assertEqual(Task.objects.count(), 0)
