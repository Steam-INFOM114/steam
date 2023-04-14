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

    def test_task_form_start_date_before_project_start_date_error(self):
        """Test that the create task form is invalid with a start_date before the project start_date."""
        invalid_data = self.valid_data.copy()
        invalid_data['start_date'] = self.project.start_date - \
            timezone.timedelta(days=1)  # start_date before project start_date
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

    def test_task_form_end_date_after_project_end_date_error(self):
        """Test that the create task form is invalid with an end_date after the project end_date."""
        invalid_data = self.valid_data.copy()
        invalid_data['end_date'] = self.project.end_date + \
            timezone.timedelta(days=1)  # end_date after project end_date
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

    def test_task_form_no_project_error(self):
        """Test that the create task form is invalid with no project."""
        invalid_data = self.valid_data.copy()
        invalid_data['project'] = None
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertIn('project', form.errors)

    def test_task_form_no_name_error(self):
        """Test that the create task form is invalid with no name."""
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = ''
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertIn('name', form.errors)

    def test_task_form_name_only_spaces_error(self):
        """Test that the create task form is invalid with a name that only contains spaces."""
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = '   '
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertIn('name', form.errors)

    def test_task_form_name_too_long_error(self):
        """Test that the create task form is invalid with a name that is too long."""
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = 'a' * 101
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertIn('name', form.errors)

    def test_task_form_start_date_but_no_end_date_error(self):
        """Test that the create task form is invalid with a start_date but no end_date."""
        invalid_data = self.valid_data.copy()
        invalid_data['end_date'] = ''
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertIn('end_date', form.errors)

    def test_task_form_end_date_but_no_start_date_error(self):
        """Test that the create task form is invalid with an end_date but no start_date."""
        invalid_data = self.valid_data.copy()
        invalid_data['start_date'] = ''
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertIn('start_date', form.errors)

    def test_task_form_start_date_before_project_start_date_error(self):
        """Test that the create task form is invalid with a start_date before the project start_date."""
        invalid_data = self.valid_data.copy()
        invalid_data['start_date'] = self.project.start_date - \
            timezone.timedelta(days=1)
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertIn('start_date', form.errors)

    def test_task_form_start_date_after_project_end_date_error(self):
        """Test that the create task form is invalid with a start_date after the project end_date."""
        invalid_data = self.valid_data.copy()
        invalid_data['start_date'] = self.project.end_date + \
            timezone.timedelta(days=1)
        invalid_data['end_date'] = invalid_data['start_date'] + \
            timezone.timedelta(days=1)
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

    def test_task_form_end_date_after_project_end_date_error(self):
        """Test that the create task form is invalid with an end_date after the project end_date."""
        invalid_data = self.valid_data.copy()
        invalid_data['end_date'] = self.project.end_date + \
            timezone.timedelta(days=1)
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)
        self.assertIn('end_date', form.errors)

    def test_task_form_end_date_before_project_start_date_error(self):
        """Test that the create task form is invalid with an end_date before the project start_date."""
        invalid_data = self.valid_data.copy()
        invalid_data['start_date'] = self.project.start_date - \
            timezone.timedelta(days=2)
        invalid_data['end_date'] = self.project.start_date - \
            timezone.timedelta(days=1)
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

    def test_task_form_start_date_equals_end_date_is_valid(self):
        """Test that the create task form is valid with a start_date equal to the end_date."""
        self.valid_data['start_date'] = self.valid_data['end_date']
        form = TaskForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_task_form_start_date_equals_project_start_date_is_valid(self):
        """Test that the create task form is valid with a start_date equal to the project start_date."""
        self.valid_data['start_date'] = self.project.start_date
        form = TaskForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_task_form_end_date_equals_project_end_date_is_valid(self):
        """Test that the create task form is valid with an end_date equal to the project end_date."""
        self.valid_data['end_date'] = self.project.end_date
        form = TaskForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
