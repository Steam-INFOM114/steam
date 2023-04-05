from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Project, Task
from django.utils import timezone
from django.core.exceptions import ValidationError


class TaskModelTest(TestCase):
    def setUp(self):
        """
        Setup method that creates a sample Task instance
        """
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
        self.task = Task.objects.create(
            name='Test Task',
            description='This is a test task',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            status='1',
            project=self.project
        )

    def test_task_model_instance(self):
        """
        Test that a Task instance can be created and saved to the database
        """
        task = Task.objects.create(
            name='Test Task 2',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=1),
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
        self.assertEqual(task.start_date, timezone.now().date())
        self.assertEqual(task.end_date, timezone.now().date() +
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
            start_date=timezone.now().date() + timezone.timedelta(days=1),
            end_date=timezone.now().date(),
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
        with self.assertRaises(ValidationError):
            task = Task(
                name='Test Task 2',
                start_date=timezone.now().date(),
                end_date=timezone.now().date() + timezone.timedelta(days=1),
                status='1',
            )
            with self.assertRaises(ValidationError):
                task.full_clean()

    def test_task_no_name_raises_validation_error(self):
        """
        Test that a Task cannot be created without a name
        """
        task = Task(
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=1),
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
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=1),
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
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=1),
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
            start_date=timezone.now().date(),
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
            end_date=timezone.now().date() + timezone.timedelta(days=1),
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
            end_date=timezone.now().date() + timezone.timedelta(days=1),
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
            start_date=timezone.now().date(),
            end_date=self.project.end_date + timezone.timedelta(days=1),
            status='1',
            project=self.project
        )
        with self.assertRaises(ValidationError):
            task.full_clean()
