from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_test_case import BaseTestCase


class LoginTests(BaseTestCase):
    def test_login_verified_user(self):
        # ログインページにアクセス
        self.selenium.get(f"{self.live_server_url}/accounts/login/")

        # 認証済みユーザーでログイン
        self.selenium.find_element(By.NAME, "login").send_keys("verifieduser")
        self.selenium.find_element(
            By.NAME, "password").send_keys("testpass123")

        submit_button = self.selenium.find_element(
            By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # ホームページにリダイレクトされることを確認
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.current_url == f"{self.live_server_url}/"
        )

    def test_login_with_nonexistent_user(self):
        # ログインページにアクセス
        self.selenium.get(f"{self.live_server_url}/accounts/login/")

        # 存在しないユーザー情報を入力
        self.selenium.find_element(By.NAME, "login").send_keys(
            "nonexistent@example.com")
        self.selenium.find_element(
            By.NAME, "password").send_keys("wrongpassword123")

        # ログインボタンをクリック
        self.selenium.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()

        # エラーメッセージが表示されることを確認
        error_message = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        self.assertTrue(error_message.is_displayed())
        self.assertIn("入力されたメールアドレスもしくはパスワードが正しくありません。", error_message.text)

        # ログインページに留まっていることを確認
        self.assertEqual(
            self.selenium.current_url,
            f"{self.live_server_url}/accounts/login/"
        )
