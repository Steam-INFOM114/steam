from django.test import TestCase
from core.models import Project, Task
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskDeleteViewTest(TestCase):
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
        self.task = Task.objects.create(name='Task 1', description='Description for Task 1',
                                        start_date=timezone.now().date(), end_date=timezone.now().date(),
                                        status='1', project=self.project)
        self.url = reverse('task-delete', args=[self.task.id])

    def test_delete_task_view_success(self):
        """Test that the delete task view deletes a task."""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task-list'))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_task_view_not_found(self):
        """Test that the delete task view returns a 404 if the task does not exist."""
        response = self.client.post(reverse('task-delete', args=[100]))
        self.assertEqual(response.status_code, 404)
