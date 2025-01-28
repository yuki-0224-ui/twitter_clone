from django.test import TestCase
from django.core.exceptions import ValidationError
from tweets.models import CustomUser
from django.db import IntegrityError


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.valid_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'display_name': 'Test User',
        }

    def test_create_user_success(self):
        user = CustomUser.objects.create_user(**self.valid_user_data)

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_username_unique(self):
        CustomUser.objects.create_user(**self.valid_user_data)

        new_user_data = self.valid_user_data.copy()
        new_user_data['email'] = 'another@example.com'

        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(**new_user_data)

    def test_email_unique(self):
        CustomUser.objects.create_user(**self.valid_user_data)

        new_user_data = self.valid_user_data.copy()
        new_user_data['username'] = 'another_user'

        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(**new_user_data)

    def test_username_max_length(self):
        new_user_data = self.valid_user_data.copy()
        new_user_data['username'] = 'a' * 16

        with self.assertRaises(ValidationError):
            user = CustomUser(**new_user_data)
            user.full_clean()

    def test_display_name_auto_set(self):
        new_user_data = self.valid_user_data.copy()
        del new_user_data['display_name']

        user = CustomUser.objects.create_user(**new_user_data)

        self.assertEqual(user.display_name, user.username)
