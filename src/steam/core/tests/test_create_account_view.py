from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class TestCreateAccountView(TestCase):

    def setUp(self):
        self.user = User(username='test_username', password='test_password', email='test@example.com', first_name='test_firstname', last_name='test_lastname')

    # REGISTER

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_view_post(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password, 'email': self.user.email, 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 302)
        self.assertEquals(User.objects.count(), 1)
        last_user = User.objects.last()
        self.assertEquals(last_user.username, self.user.username)
        self.assertEquals(last_user.email, self.user.email)
        self.assertEquals(last_user.first_name, self.user.first_name)
        self.assertEquals(last_user.last_name, self.user.last_name)

        self.assertRedirects(response, reverse('project-list'))

    def test_register_view_post_password_invalid(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': 'invalid_password', 'email': self.user.email, 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_post_username_empty_invalid(self):
        self.user.save()
        response = self.client.post(reverse('register'), {'username': '', 'password1': self.user.password, 'password2': self.user.password, 'email': self.user.email, 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_post_username_exists_invalid(self):
        self.user.save()
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password, 'email': self.user.email, 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 1)

    def test_register_view_post_username_spaces_only_invalid(self):
        response = self.client.post(reverse('register'), {'username': '   ', 'password1': self.user.password, 'password2': self.user.password, 'email': self.user.email, 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_post_username_too_long_invalid(self):
        response = self.client.post(reverse('register'), {'username': 'a'*151, 'password1': self.user.password, 'password2': self.user.password, 'email': self.user.email, 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_post_password_empty_invalid(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': '', 'password2': '', 'email': self.user.email, 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_post_password_too_short_invalid(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': 'a'*7, 'password2': 'a'*7, 'email': self.user.email, 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_post_password_entirely_numeric_invalid(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': '12345678', 'password2': '12345678', 'email': self.user.email, 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_post_password_same_as_username_invalid(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.username, 'password2': self.user.username, 'email': self.user.email, 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_post_email_empty_invalid(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password, 'email': '', 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_post_email_invalid1(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password, 'email': 'test', 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_post_email_invalid1(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password, 'email': 'test@', 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_post_email_invalid1(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password, 'email': 'test@example', 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_post_email_invalid1(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password, 'email': 'test@example.', 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_post_email_invalid1(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password, 'email': '@example.com', 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_post_email_invalid1(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password, 'email': 'example.com', 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_post_email_invalid1(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password, 'email': '.com', 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_post_email_invalid1(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password, 'email': 'test@.com', 'first_name': self.user.first_name, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_first_name_empty_invalid(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password, 'email': self.user.email, 'first_name': '', 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_first_name_too_long_invalid(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password, 'email': self.user.email, 'first_name': 'a'*31, 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_first_name_spaces_only_invalid(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password, 'email': self.user.email, 'first_name': '     ', 'last_name': self.user.last_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_last_name_empty_invalid(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password, 'email': self.user.email, 'first_name': self.user.first_name, 'last_name': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_last_name_too_long_invalid(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password, 'email': self.user.email, 'first_name': self.user.first_name, 'last_name': 'a' * 31})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    def test_register_view_last_name_spaces_only_invalid(self):
        response = self.client.post(reverse('register'), {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password, 'email': self.user.email, 'first_name': self.user.first_name, 'last_name': '     '})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEquals(User.objects.count(), 0)

    # LOGIN

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_post(self):
        self.user.save()
        response = self.client.post(reverse('login'), {'username': self.user.username, 'password': self.user.password})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('project-list'))

    def test_login_view_post_invalid(self):
        self.user.save()
        response = self.client.post(reverse('login'), {'username': self.user.username, 'password': 'invalid_password'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_post_already_logged_in(self):
        self.user.save()
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.post(reverse('login'), {'username': self.user.username, 'password': self.user.password})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('project-list'))

    # LOGOUT

    def test_logout_view_post(self):
        self.user.save()
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('project-list'))

    def test_logout_view_post_not_logged_in(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('project-list'))



