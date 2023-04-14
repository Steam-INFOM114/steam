from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()
class TestUserModel(TestCase):

    def setUp(self):
        self.user = User(username='test_username', password='test_password', email='test@example.com', first_name='test_firstname', last_name='test_lastname')

    def test_user_valid(self):
        new_user = User.objects.create_user(self.user)
        self.assertEqual(new_user.username, self.user.username)
        self.assertEqual(new_user.email, self.user.email)
        self.assertEqual(new_user.first_name, self.user.first_name)
        self.assertEqual(new_user.last_name, self.user.last_name)

    def test_user_password_not_raw_stored(self):
        new_user = User.objects.create_user(self.user)
        self.assertNotEqual(new_user.password, self.user.password)

    def test_user_username_empty_raises_validation_error(self):
        self.user.username = ''
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_username_too_long_raises_validation_error(self):
        self.user.username = 'a' * 151
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_username_space_only_raises_validation_error(self):
        self.user.username = ' '
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_password_empty_raises_validation_error(self):
        self.user.password = ''
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_password_too_short_raises_validation_error(self):
        self.user.password = 'a' * 7
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_password_entirely_numeric_raises_validation_error(self):
        self.user.password = '12345678'
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_password_same_as_username_raise_validation_error(self):
        self.user.password = self.user.username
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_email_empty_raises_validation_error(self):
        self.user.email = ''
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_email_invalid_raises_validation_error1(self):
        self.user.email = 'test'
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_email_invalid_raises_validation_error2(self):
        self.user.email = 'test@'
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_email_invalid_raises_validation_error3(self):
        self.user.email = 'test@example'
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_email_invalid_raises_validation_error4(self):
        self.user.email = 'test@example.'
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_email_invalid_raises_validation_error5(self):
        self.user.email = '@example.com'
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_email_invalid_raises_validation_error6(self):
        self.user.email = 'test@.com'
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_email_invalid_raises_validation_error7(self):
        self.user.email = 'example.com'
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_email_invalid_raises_validation_error8(self):
        self.user.email = '.com'
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_first_name_empty_raises_validation_error(self):
        self.user.first_name = ''
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_first_name_too_long_raises_validation_error(self):
        self.user.first_name = 'a' * 31
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_firstname_space_only_raises_validation_error(self):
        self.user.first_name = ' '
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_last_name_empty_raises_validation_error(self):
        self.user.last_name = ''
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_last_name_too_long_raises_validation_error(self):
        self.user.last_name = 'a' * 31
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)

    def test_user_lastname_space_only_raises_validation_error(self):
        self.user.last_name = ' '
        with self.assertRaises(ValidationError):
            User.objects.create_user(self.user)
