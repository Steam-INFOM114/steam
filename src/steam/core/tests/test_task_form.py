from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Project
from core.forms import TaskForm
from django.utils import timezone

class TaskFormTest(TestCase):
    def setUp(self):
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

    def test_task_form_fields(self):
        """Test that the create_task.html template contains the correct number of form fields."""
        fields = TaskForm().fields.keys()
        expected_fields = ['name', 'description',
                           'start_date', 'end_date', 'status', 'project']
        self.assertCountEqual(fields, expected_fields)

    def test_task_form_valid_data(self):
        """Test that the create task form is valid with valid data."""
        form = TaskForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_task_form_empty_data(self):
        """Test that the create task form is invalid with empty data."""
        form = TaskForm(data={})
        self.assertFalse(form.is_valid())
        # Expect an error for the required name field
        self.assertIn('name', form.errors)
        # Expect an error for the required start_date field
        self.assertIn('start_date', form.errors)
        # Expect an error for the required end_date field
        self.assertIn('end_date', form.errors)
        # Expect an error for the required status field
        self.assertIn('status', form.errors)
        # Expect an error for the required status field
        self.assertIn('project', form.errors)

    def test_task_form_end_date_before_start_date(self):
        """Test that the create task form is invalid with an end_date before start_date."""
        invalid_data = self.valid_data.copy()
        invalid_data['start_date'] = self.valid_data['start_date'] + \
            timezone.timedelta(days=2)  # end_date before start_date
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

    def test_task_form_invalid_status(self):
        """Test that the create task form is invalid with an invalid status choice."""
        invalid_data = self.valid_data.copy()
        invalid_data['status'] = '4'  # Invalid choice
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        # Expect an error for the status field
        self.assertIn('status', form.errors)
