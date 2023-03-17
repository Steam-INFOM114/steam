from django.test import TestCase
from ..models import Project
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class ProjectModelTest(TestCase):
    def setUp(self):
        # Create some users
        users = [User(username='user{}'.format(i)) for i in range(3)]

    def test_valid_project_with_all_fields(self):
        project = Project(
            name='My project',
            description='My description',
            start_date='2018-01-01',
            end_date='2019-01-01',
            owner=self.users[0],
            members=[self.users[1], self.users[2]])
        try:
            project.full_clean()
        except ValidationError:
            self.fail('full_clean() raised ValidationError unexpectedly!')

    def test_string_representation(self):
        project = Project(name='My project')
        self.assertEqual(str(project), project.name)

    def test_name_is_empty_and_raises_validation_error(self):
        project = Project(name='')
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_name_is_too_long_and_raises_validation_error(self):
        project = Project(name='a' * 256)
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_start_date_is_after_end_date_and_raises_validation_error(self):
        project = Project(start_date='2019-01-01', end_date='2018-01-01')
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_start_date_is_before_end_date_and_does_not_raise_validation_error(self):
        project = Project(start_date='2018-01-01', end_date='2019-01-01')
        try:
            project.full_clean()
        except ValidationError:
            self.fail('full_clean() raised ValidationError unexpectedly!')

    def test_start_date_is_equal_to_end_date_and_does_not_raise_validation_error(self):
        project = Project(start_date='2018-01-01', end_date='2018-01-01')
        try:
            project.full_clean()
        except ValidationError:
            self.fail('full_clean() raised ValidationError unexpectedly!')

    def test_start_date_is_none_and_raises_validation_error(self):
        project = Project(start_date=None)
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_end_date_is_none_and_raises_validation_error(self):
        project = Project(end_date=None)
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_owner_is_member_and_raises_validation_error(self):
        project = Project(
            name='My project',
            description='My description',
            start_date='2018-01-01',
            end_date='2019-01-01',
            owner=self.users[0],
            members=[self.users[0], self.users[1]])
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_two_same_members_and_raises_validation_error(self):
        project = Project(
            name='My project',
            description='My description',
            start_date='2018-01-01',
            end_date='2019-01-01',
            owner=self.users[0],
            members=[self.users[1], self.users[1]])
        with self.assertRaises(ValidationError):
            project.full_clean()
