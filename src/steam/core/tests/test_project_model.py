from django.test import TestCase
from core.models import Project
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class TestProjectModel(TestCase):
    def setUp(self):
        self.today = timezone.now().date()
        # Create some users
        self.users = [User(username='user{}'.format(i), email='user{}@exampl.com'.format(i), password='password') for i in range(3)]
        for user in self.users:
            user.save()

    def test_valid_project_with_all_fields(self):
        project = Project(
            name='My project',
            description='My description',
            start_date='2018-01-01',
            end_date='2019-01-01',
            owner=self.users[0])
        try:
            project.full_clean()
            project.save()
            project.members.set([self.users[1], self.users[2]])
        except ValidationError:
            self.fail('full_clean() raised ValidationError unexpectedly!')

    def test_string_representation(self):
        project = Project(name='My project', owner=self.users[0], start_date='2018-01-01', end_date='2019-01-01')
        self.assertEqual(str(project), project.name)

    def test_name_is_empty_and_raises_validation_error(self):
        project = Project(name='', owner=self.users[0], start_date='2018-01-01', end_date='2019-01-01')
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_name_is_too_long_and_raises_validation_error(self):
        project = Project(name='a' * 256, owner=self.users[0], start_date='2018-01-01', end_date='2019-01-01')
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_start_date_is_after_end_date_and_raises_validation_error(self):
        project = Project(name='My project', owner=self.users[0], start_date='2019-01-01', end_date='2018-01-01')
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_start_date_is_before_end_date_and_does_not_raise_validation_error(self):
        project = Project(name='My project', owner=self.users[0], start_date='2018-01-01', end_date='2019-01-01')
        try:
            project.full_clean()
        except ValidationError:
            self.fail('full_clean() raised ValidationError unexpectedly!')

    def test_start_date_is_equal_to_end_date_and_raise_validation_error(self):
        project = Project(name='My project', owner=self.users[0], start_date='2018-01-01', end_date='2018-01-01')
        with self.assertRaises(ValidationError):
            project.full_clean()

    # def test_start_date_is_none_and_raises_validation_error(self):
    #     project = Project(start_date=None)
    #     with self.assertRaises(ValidationError):
    #         project.full_clean()

    # def test_end_date_is_none_and_raises_validation_error(self):
    #     project = Project(end_date=None)
    #     with self.assertRaises(ValidationError):
    #         project.full_clean()

    def test_owner_is_member_and_raises_validation_error(self):
        project = Project(
            name='My project',
            description='My description',
            start_date='2018-01-01',
            end_date='2019-01-01',
            owner=self.users[0])
        project.save()
        with self.assertRaises(ValidationError):
            project.members.set([self.users[0]])

    def test_member_is_owner_and_raises_validation_error(self):
        project = Project(
            name='My project',
            description='My description',
            start_date='2018-01-01',
            end_date='2019-01-01',
            owner=self.users[0])
        project.save()
        project.members.set([self.users[1]])
        project.owner = self.users[1]
        with self.assertRaises(ValidationError):
            project.full_clean()


    def test_two_same_members_and_only_one_is_added(self):
        project = Project(
            name='My project',
            description='My description',
            start_date='2018-01-01',
            end_date='2019-01-01',
            owner=self.users[0])
        project.save()
        project.members.set([self.users[1], self.users[1]])
        self.assertEqual(project.members.count(), 1)

    def test_key_field_is_generated_on_save(self):
        """Test that the Project model generates a key when saved."""
        first_project = Project(
            name='Test Project 1',
            description='First test project',
            start_date=self.today,
            end_date=self.today + timezone.timedelta(days=14),
            owner=self.users[0],
        )

        # Check that the key is empty before saving
        self.assertEqual(first_project.key, '')
        # Save the project and check that the key has been generated
        first_project.save()
        self.assertNotEqual(first_project.key, '')

    def test_key_field_is_unique(self):
        """Test that the key field is unique."""
        first_project = Project(
            name='Test Project 1',
            description='First test project',
            start_date=self.today,
            end_date=self.today + timezone.timedelta(days=14),
            owner=self.users[0],
        )
        first_project.save()
        # Create another project with the same name and owner
        second_project = Project(
            name='Test Project 1',
            description='Another test project.',
            start_date=self.today,
            end_date=self.today + timezone.timedelta(days=14),
            owner=self.users[0],
        )
        # Set the key to be the same as the first project
        second_project.key = first_project.key
        # Try to save the second project and expect a Validation error
        with self.assertRaises(ValidationError):
            second_project.save()
