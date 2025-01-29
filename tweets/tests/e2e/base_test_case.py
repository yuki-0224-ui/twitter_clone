from allauth.account.models import EmailAddress, EmailConfirmation
from django.core import mail
from django.contrib.auth import get_user_model
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class BaseTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--user-data-dir=/tmp/chrome-data')
        cls.selenium = WebDriver(options=chrome_options)
        cls.selenium.set_window_size(1920, 1080)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.User = get_user_model()

        mail.outbox = []

        # メール認証済みユーザーの作成
        self.verified_user = self.User.objects.create_user(
            username='verifieduser',
            email='verified@example.com',
            password='testpass123'
        )

        EmailAddress.objects.create(
            user=self.verified_user,
            email='verified@example.com',
            verified=True,
            primary=True
        )

    def tearDown(self):
        self.User.objects.all().delete()
        EmailAddress.objects.all().delete()
        EmailConfirmation.objects.all().delete()
        super().tearDown()
