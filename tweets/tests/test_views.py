from django.test import TestCase, Client
from django.urls import reverse
from tweets.models import CustomUser, Tweet


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('tweets:account_signup')
        self.login_url = reverse('tweets:account_login')
        self.home_url = reverse('tweets:home')

        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        self.login_data = {
            'login': 'testuser',
            'password': 'testpass123'
        }

    def test_signup_success(self):
        response = self.client.post(self.signup_url, self.user_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(
            username='testuser').exists())

    def test_signup_fail_duplicate_username(self):
        self.client.post(self.signup_url, self.user_data)

        response = self.client.post(self.signup_url, self.user_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "このユーザー名は既に使用されています")

    def test_login_success(self):
        self.client.post(self.signup_url, self.user_data)

        response = self.client.post(self.login_url, self.login_data)

        self.assertEqual(response.status_code, 302)

    def test_login_fail_wrong_password(self):
        self.client.post(self.signup_url, self.user_data)

        wrong_data = self.login_data.copy()
        wrong_data['password'] = 'wrongpass'

        response = self.client.post(self.login_url, wrong_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "入力されたユーザー名もしくはパスワードが正しくありません。")

    def test_tweet_create_success(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.client.force_login(user)

        tweet_data = {'content': 'Test tweet'}
        response = self.client.post(self.home_url, tweet_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tweet.objects.filter(content='Test tweet').exists())

    def test_tweet_create_fail_too_long(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.client.force_login(user)

        tweet_data = {'content': 'a' * 141}
        response = self.client.post(self.home_url, tweet_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "この値は 140 文字以下でなければなりません")
