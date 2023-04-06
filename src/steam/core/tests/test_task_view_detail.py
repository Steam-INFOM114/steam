from django.test import TestCase
from django.urls import reverse
from core.models import Project,Task
from django.utils import timezone
from django.contrib.auth.models import User

class TestTaskViewDetail(TestCase):
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
        self.url = reverse('task', args=[self.task.id])

    def test_task_view_detail_success(self):
        """Test that the task view detail returns a 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task.html')
        self.assertContains(response, self.task.name)
        self.assertContains(response, self.task.description)
        self.assertContains(response, self.project)
        self.assertContains(response, self.task.get_status_display())
        self.assertContains(response, self.task.start_date)
        self.assertContains(response, self.task.end_date)

    def test_task_view_detail_not_found(self):
        """Test that the task view detail returns a 404 if the task does not exist."""
        response = self.client.get(reverse('task', args=[100]))
        self.assertEqual(response.status_code, 404)

