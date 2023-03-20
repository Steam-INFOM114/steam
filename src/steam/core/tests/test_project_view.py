from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Project

class TestProjectView(TestCase):
    def setUp(self):
        # Create some users
        self.users = [User(username='user{}'.format(i)) for i in range(3)]
        for user in self.users:
            user.save()

        # Create some projects
        self.projects = [Project(
            name='Project {}'.format(i),
            description='This is project {}.'.format(i),
            start_date='2018-01-01',
            end_date='2019-01-01',
            owner=self.users[0],) for i in range(3)]
        for project in self.projects:
            project.save()
            project.members.set([self.users[1], self.users[2]])

    # CREATE

    def test_project_create_view(self):
        response = self.client.get(reverse('project-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/create_update.html')

    def test_project_create_view_post(self):
        response = self.client.post(reverse('project-create'), {
            'name': 'New project',
            'description': 'This is a new project.',
            'start_date': '2018-01-01',
            'end_date': '2019-01-01',
            'owner': self.users[0].pk,
            'members': [self.users[1].pk, self.users[2].pk]
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.count(), len(self.projects) + 1)

        new_project = Project.objects.last()
        self.assertEqual(new_project.name, 'New project')
        self.assertEqual(new_project.description, 'This is a new project.')
        self.assertEqual(new_project.start_date, date(2018, 1, 1))
        self.assertEqual(new_project.end_date, date(2019, 1, 1))
        self.assertEqual(new_project.owner, self.users[0])
        self.assertQuerysetEqual(new_project.members.all(), map(repr, [self.users[1], self.users[2]]), ordered=False)

        # Get the page after the post and check if the page contains the new project
        expected_url = reverse('project-list')
        self.assertRedirects(response, expected_url)
        response = self.client.get(expected_url)
        self.assertContains(response, new_project.name)
        self.assertContains(response, new_project.description)
        # self.assertContains(response, new_project.start_date)
        # self.assertContains(response, new_project.end_date)
        self.assertContains(response, self.users[0].username)

    # READ

    def test_project_list_view(self):
        response = self.client.get(reverse('project-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/list.html')
        self.assertQuerysetEqual(response.context['object_list'], map(repr, self.projects), ordered=False)
        for project in self.projects:
            self.assertContains(response, project.name)
            self.assertContains(response, project.description)
            # self.assertContains(response, project.start_date)
            # self.assertContains(response, project.end_date)
            self.assertContains(response, project.owner.username)

    def test_project_detail_view(self):
        response = self.client.get(reverse('project-detail', kwargs={'pk': self.projects[0].pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/detail.html')
        self.assertEqual(response.context['object'], self.projects[0])
        project = self.projects[0]
        self.assertContains(response, project.name)
        self.assertContains(response, project.description)
        # self.assertContains(response, project.start_date)
        # self.assertContains(response, project.end_date)
        self.assertContains(response, project.owner.username)
        for member in project.members.all():
            self.assertContains(response, member.username)

    # UPDATE

    def test_project_update_view(self):
        response = self.client.get(reverse('project-update', kwargs={'pk': self.projects[0].pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/create_update.html')
        self.assertEqual(response.context['object'], self.projects[0])

    def test_project_update_view_post(self):
        response = self.client.post(reverse('project-update', kwargs={'pk': self.projects[0].pk}), {
            'name': 'Updated project',
            'description': 'This is an updated project.',
            'start_date': '2020-01-01',
            'end_date': '2021-01-01',
            'owner': self.users[1].pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.count(), len(self.projects))

        updated_project = Project.objects.get(pk=self.projects[0].pk)

        updated_project.members.set([self.users[2], self.users[0]])

        self.assertEqual(updated_project.name, 'Updated project')
        self.assertEqual(updated_project.description, 'This is an updated project.')
        self.assertEqual(updated_project.start_date, date(2020, 1, 1))
        self.assertEqual(updated_project.end_date, date(2021, 1, 1))
        self.assertEqual(updated_project.owner, self.users[1])
        self.assertQuerysetEqual(updated_project.members.all(), map(repr, [self.users[2], self.users[0]]), ordered=False)

        # Get the page after the post and check if the page contains the updated project
        expected_url = reverse('project-list')
        self.assertRedirects(response, expected_url)
        response = self.client.get(expected_url)
        self.assertContains(response, updated_project.name)
        self.assertContains(response, updated_project.description)
        # self.assertContains(response, updated_project.start_date)
        # self.assertContains(response, updated_project.end_date)
        self.assertContains(response,self.users[1].username)

    # DELETE

    def test_project_delete_view_post(self):
        response = self.client.post(reverse('project-delete', kwargs={'pk': self.projects[0].pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.count(), len(self.projects) - 1)

        # Get the page after the post and check if the page does not contain the deleted project
        expected_url = reverse('project-list')
        self.assertRedirects(response, expected_url)
        response = self.client.get(expected_url)
        self.assertNotContains(response, self.projects[0].name)
        self.assertNotContains(response, self.projects[0].description)
        # self.assertNotContains(response, self.projects[0].start_date)
        # self.assertNotContains(response, self.projects[0].end_date)
        self.assertNotContains(response, self.projects[0].owner.username)
        for member in self.projects[0].members.all():
            self.assertNotContains(response, member.username)
