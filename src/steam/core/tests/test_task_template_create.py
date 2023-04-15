from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Project, Task
from django.urls import reverse
from django.utils import timezone


class TaskCreateTemplateTest(TestCase):
    def setUp(self):
        self.url = reverse('task-create')
        self.response = self.client.get(self.url)
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

    def test_create_task_template_title(self):
        """Test that the create_task.html template's title is rendered."""
        self.assertContains(self.response, 'Créer une tâche')

    def test_create_task_template_form(self):
        """Test that the create_task.html template contains a form."""
        self.assertContains(
            self.response, '<form')  # Expect a form to be displayed

    def test_create_task_template_form_labels(self):
        """Test that the create_task.html template contains the correct form labels."""
        labels = self.response.content.decode().lower()
        self.assertIn('nom', labels)
        self.assertIn('description', labels)
        self.assertIn('date de début', labels)
        self.assertIn('date de fin', labels)
        self.assertIn('statut', labels)
        self.assertIn('projet', labels)

    def test_create_task_template_fields(self):
        """Test that the create task template contains all the input fields in the form."""
        response = self.client.get(self.url)
        self.assertContains(response, '<input', count=4)
        self.assertContains(response, 'name="name"', count=1)
        self.assertContains(response, 'name="description"', count=1)
        self.assertContains(response, 'name="start_date"', count=1)
        self.assertContains(response, 'name="end_date"', count=1)
        self.assertContains(response, 'name="status"', count=1)
        self.assertContains(response, 'name="project"', count=1)

    def test_create_task_template_submit_button(self):
        """Test that the create task template contains the submit button."""
        response = self.client.get(self.url)
        submit_button_regex = r'<button(?=.*type="submit")(?=.*Créer)[^>]*>.*</button>'
        self.assertRegex(response.content.decode('utf-8'), submit_button_regex)

    def test_create_task_template_invalid_date_format(self):
        """Test that the create task template shows error message for invalid date formats"""
        invalid_data = self.valid_data.copy()
        invalid_data['start_date'] = '2022/03/15'
        invalid_data['end_date'] = '2022/03/16'
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid date.', count=2)

    def test_create_task_template_required_fields(self):
        """Test that the create task template shows error message for missing required fields."""
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
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_name_spaces_only_error(self):
        """Test that the create task template shows error message for name with spaces only."""
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = '    '
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_name_too_long_error(self):
        """Test that the create task template shows error message for name too long."""
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = 'a' * 101
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_start_date_but_no_end_date_error(self):
        """Test that the create task template shows error message when a start date is set but no end date."""
        invalid_data = self.valid_data.copy()
        invalid_data['end_date'] = ''
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_end_date_but_no_start_date_error(self):
        """Test that the create task template shows error message when an end date is set but no start date."""
        invalid_data = self.valid_data.copy()
        invalid_data['start_date'] = ''
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_end_date_after_project_end_date_error(self):
        """Test that the create task template shows error message when the end date is after the project end date."""
        invalid_data = self.valid_data.copy()
        invalid_data['end_date'] = self.project.end_date + timezone.timedelta(days=1)
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_end_date_before_project_start_date_error(self):
        """Test that the create task template shows error message when the end date is before the project start date."""
        invalid_data = self.valid_data.copy()
        invalid_data['start_date'] = self.project.start_date - timezone.timedelta(days=2)
        invalid_data['end_date'] = self.project.start_date - timezone.timedelta(days=1)
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_start_date_after_project_end_date_error(self):
        """Test that the create task template shows error message when the start date is after the project end date."""
        invalid_data = self.valid_data.copy()
        invalid_data['start_date'] = self.project.end_date + timezone.timedelta(days=1)
        invalid_data['end_date'] = invalid_data['start_date'] + timezone.timedelta(days=1)
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_start_date_before_project_start_date_error(self):
        """Test that the create task template shows error message when the start date is before the project start date."""
        invalid_data = self.valid_data.copy()
        invalid_data['start_date'] = self.project.start_date - timezone.timedelta(days=1)
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_start_date_equals_end_date_is_valid(self):
        """Test that the create task template allows a start date that is the same as the end date."""
        self.valid_data['start_date'] = self.valid_data['end_date']
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)

        # Get the page after the post and check if the page contains the new task
        expected_url = reverse('task-list')
        self.assertRedirects(response, expected_url)
        response = self.client.get(expected_url)
        self.assertTemplateUsed(response, 'tasks/tasks.html')
        self.assertContains(response, self.valid_data['name'])

    def test_create_task_start_date_equals_project_start_date_is_valid(self):
        """Test that the create task template allows a start date that is the same as the project start date."""
        self.valid_data['start_date'] = self.project.start_date
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)

        # Get the page after the post and check if the page contains the new task
        expected_url = reverse('task-list')
        self.assertRedirects(response, expected_url)
        response = self.client.get(expected_url)
        self.assertTemplateUsed(response, 'tasks/tasks.html')
        self.assertContains(response, self.valid_data['name'])

    def test_create_task_end_date_equals_project_end_date(self):
        """Test that the create task template allows an end date that is the same as the project end date."""
        self.valid_data['end_date'] = self.project.end_date
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)

        # Get the page after the post and check if the page contains the new task
        expected_url = reverse('task-list')
        self.assertRedirects(response, expected_url)
        response = self.client.get(expected_url)
        self.assertTemplateUsed(response, 'tasks/tasks.html')
        self.assertContains(response, self.valid_data['name'])
