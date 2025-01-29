from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allauth.account.models import EmailAddress
from django.core import mail
import re
from .base_test_case import BaseTestCase


class SignupTests(BaseTestCase):
    def test_signup_success_and_email_verification(self):
        test_username = "e2e_test_user"
        test_email = "e2e_test@example.com"
        test_password = "e2epass123"

        # サインアップページにアクセス
        self.selenium.get(f"{self.live_server_url}/accounts/signup/")

        # フォームに情報を入力
        self.selenium.find_element(
            By.NAME, "username").send_keys(test_username)
        self.selenium.find_element(By.NAME, "email").send_keys(test_email)
        self.selenium.find_element(
            By.NAME, "password1").send_keys(test_password)
        self.selenium.find_element(
            By.NAME, "password2").send_keys(test_password)

        # サインアップボタンをクリック
        submit_button = self.selenium.find_element(
            By.CSS_SELECTOR, "button[type='submit']")
        self.selenium.execute_script(
            "arguments[0].scrollIntoView(true);", submit_button)
        submit_button.click()

        # メール確認ページの表示を確認
        heading = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(), 'メールアドレスの確認')]")
            )
        )
        self.assertTrue(heading.is_displayed())

        # ユーザーとメールアドレスが作成されていることを確認
        user = self.User.objects.get(username=test_username)
        email_address = EmailAddress.objects.get(user=user, email=test_email)

        # 確認メールが送信されたことを確認
        self.assertEqual(len(mail.outbox), 1)
        confirmation_mail = mail.outbox[0]

        # メール本文から確認リンクを抽出
        confirmation_link = re.search(
            r'/accounts/confirm-email/[^/\s]+/',
            confirmation_mail.body,
        ).group()

        if not confirmation_link:
            self.fail(f"確認リンクが見つかりませんでした。メール本文: {confirmation_mail.body}")

        # 確認リンクにアクセス
        self.selenium.get(f"{self.live_server_url}{confirmation_link}")

        # 確認ボタンをクリック
        confirm_button = WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[type='submit']"))
        )
        confirm_button.click()

        # メール確認完了後、ログイン状態でホームページにリダイレクトされることを確認
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.current_url == f"{self.live_server_url}/"
        )

        # メールアドレスが確認済みになっていることを確認
        email_address.refresh_from_db()
        self.assertTrue(email_address.verified)

    def test_signup_existing_user(self):
        self.selenium.get(f"{self.live_server_url}/accounts/signup/")
        self.selenium.find_element(
            By.NAME, "username").send_keys("verifieduser")
        self.selenium.find_element(
            By.NAME, "email").send_keys("new@example.com")
        self.selenium.find_element(
            By.NAME, "password1").send_keys("testpass123")
        self.selenium.find_element(
            By.NAME, "password2").send_keys("testpass123")

        submit_button = self.selenium.find_element(
            By.CSS_SELECTOR, "button[type='submit']")
        self.selenium.execute_script(
            "arguments[0].scrollIntoView(true);", submit_button)
        submit_button.click()

        # エラーメッセージの表示を確認
        error_message = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "invalid-feedback"))
        )
        self.assertIn("このユーザー名は既に使用されています", error_message.text)
