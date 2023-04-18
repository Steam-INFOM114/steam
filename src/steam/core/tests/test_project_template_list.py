from django.test import TestCase
from django.urls import reverse
from core.models import Project
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class ProjectsListTemplateTest(TestCase):
    def setUp(self):
        self.url = reverse('project-list')
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

    def test_project_list_contains_key(self):
        """Test that the list projects template contains the keys of the projects"""
        key = self.project.key
        self.client.login(username=self.user.username, password='password')

        response = self.client.get(reverse('project-list'))
        self.assertContains(response, key)
