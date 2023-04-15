from django.test import TestCase
from core.models import Project, Task
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskModelTest(TestCase):
    def setUp(self):
        """
        Setup method that creates a sample Task instance
        """
        self.now = timezone.now().date()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )
        self.project = Project.objects.create(
            name="testproject",
            description="this is a test project",
            start_date=self.now,
            end_date=self.now + timezone.timedelta(days=5),
            is_archived=False,
            owner=self.user
        )
        self.task = Task.objects.create(
            name='Test Task',
            description='This is a test task',
            start_date=self.now,
            end_date=self.now + timezone.timedelta(days=1),
            status='1',
            project=self.project
        )

    def test_task_model_instance(self):
        """
        Test that a Task instance can be created and saved to the database
        """
        task = Task.objects.create(
            name='Test Task 2',
            start_date=self.now,
            end_date=self.now + timezone.timedelta(days=1),
            status='1',
            project=self.project
        )
        self.assertEqual(Task.objects.count(), 2)

    def test_task_model_fields(self):
        """
        Test that the Task fields are correctly defined
        """
        task = Task.objects.get(name='Test Task')
        self.assertEqual(task.name, 'Test Task')
        self.assertEqual(task.description, 'This is a test task')
        self.assertEqual(task.start_date, self.now)
        self.assertEqual(task.end_date, self.now +
                         timezone.timedelta(days=1))
        self.assertEqual(task.status, '1')
        self.assertEqual(task.project.pk, self.project.pk)

    def test_task_model_str(self):
        """
        Test that the Task __str__ method returns the expected value
        """
        task = Task.objects.get(name='Test Task')
        self.assertEqual(str(task), 'Test Task')

    def test_task_start_date_after_end_date(self):
        """
        Test that the Task clean method raises a ValidationError if the start date is after the end date
        """
        task = Task.objects.create(
            name='Test Task 2',
            start_date=self.now + timezone.timedelta(days=1),
            end_date=self.now,
            status='1',
            project=self.project
        )
        with self.assertRaises(ValidationError):
            task.clean()

    def test_task_model_choices(self):
        """
        Test that the Task status field choices are correct
        """
        choices = dict(Task.CHOICES)
        self.assertEqual(
            choices, {'1': 'À commencer', '2': 'En cours', '3': 'Terminé'})

    def test_task_no_project_raises_validation_error(self):
        """
        Test that a Task cannot be created without a project
        """
        task = Task(
            name='Test Task 2',
            start_date=self.now,
            end_date=self.now + timezone.timedelta(days=1),
            status='1',
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_no_name_raises_validation_error(self):
        """
        Test that a Task cannot be created without a name
        """
        task = Task(
            start_date=self.now,
            end_date=self.now + timezone.timedelta(days=1),
            status='1',
            project=self.project
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_name_only_spaces_raises_validation_error(self):
        """
        Test that a Task cannot be created with a name that only contains spaces
        """
        task = Task(
            name='   ',
            start_date=self.now,
            end_date=self.now + timezone.timedelta(days=1),
            status='1',
            project=self.project
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_name_too_long_raises_validation_error(self):
        """
        Test that a Task cannot be created with a name that is too long
        """
        task = Task(
            name='a' * 101,
            start_date=self.now,
            end_date=self.now + timezone.timedelta(days=1),
            status='1',
            project=self.project
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_start_date_but_no_end_date_raises_validation_error(self):
        """
        Test that a Task cannot be created with a start date but no end date
        """
        task = Task(
            name='Test Task 2',
            start_date=self.now,
            status='1',
            project=self.project
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_end_date_but_no_start_date_raises_validation_error(self):
        """
        Test that a Task cannot be created with an end date but no start date
        """
        task = Task(
            name='Test Task 2',
            end_date=self.now + timezone.timedelta(days=1),
            status='1',
            project=self.project
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_start_date_before_project_start_date_raises_validation_error(self):
        """
        Test that a Task cannot be created with a start date before the project start date
        """
        task = Task(
            name='Test Task 2',
            start_date=self.project.start_date - timezone.timedelta(days=1),
            end_date=self.now + timezone.timedelta(days=1),
            status='1',
            project=self.project
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_start_date_after_project_end_date_raises_validation_error(self):
        """
        Test that a Task cannot be created with a start date after the project end date
        """
        task = Task(
            name='Test Task 2',
            start_date=self.project.end_date + timezone.timedelta(days=1),
            end_date=self.project.end_date + timezone.timedelta(days=2),
            status='1',
            project=self.project
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_end_date_after_project_end_date_raises_validation_error(self):
        """
        Test that a Task cannot be created with an end date after the project end date
        """
        task = Task(
            name='Test Task 2',
            start_date=self.now,
            end_date=self.project.end_date + timezone.timedelta(days=1),
            status='1',
            project=self.project
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_end_date_before_project_start_date_raises_validation_error(self):
        """
        Test that a Task cannot be created with an end date before the project start date
        """
        task = Task(
            name='Test Task 2',
            start_date=self.project.start_date - timezone.timedelta(days=2),
            end_date=self.project.start_date - timezone.timedelta(days=1),
            status='1',
            project=self.project
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_start_date_equals_end_date_is_valid(self):
        """
        Test that a Task can be created with a start date equal to the end date
        """
        task = Task(
            name='Test Task 2',
            start_date=self.now,
            end_date=self.now,
            status='1',
            project=self.project
        )
        task.full_clean()

    def test_task_start_date_equals_project_start_date_is_valid(self):
        """
        Test that a Task can be created with a start date equal to the project start date
        """
        task = Task(
            name='Test Task 2',
            start_date=self.project.start_date,
            end_date=self.now + timezone.timedelta(days=1),
            status='1',
            project=self.project
        )
        task.full_clean()

    def test_task_end_date_equals_project_end_date_is_valid(self):
        """
        Test that a Task can be created with an end date equal to the project end date
        """
        task = Task(
            name='Test Task 2',
            start_date=self.now,
            end_date=self.project.end_date,
            status='1',
            project=self.project
        )
        task.full_clean()
