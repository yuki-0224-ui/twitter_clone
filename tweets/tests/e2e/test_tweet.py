from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from .base_test_case import BaseTestCase


class TweetTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        # すべてのテストの前にログインする
        self.selenium.get(f"{self.live_server_url}/accounts/login/")
        self.selenium.find_element(By.NAME, "login").send_keys("verifieduser")
        self.selenium.find_element(
            By.NAME, "password").send_keys("testpass123")
        self.selenium.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()

        # ホームページにリダイレクトされることを確認
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.current_url == f"{self.live_server_url}/"
        )

    def test_tweet_success_text_only(self):
        # テキストを入力
        tweet_content = "これはテストツイートです。"
        self.selenium.find_element(
            By.ID, "post-textarea").send_keys(tweet_content)

        # 投稿ボタンをクリック
        self.selenium.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()

        # ツイートが表示されることを確認
        tweet_element = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="tweet-content"]'))
        )
        self.assertEqual(tweet_element.text.strip(), tweet_content)

    def test_tweet_success_with_image(self):
        # 画像ファイルのパスを設定
        image_path = os.path.join(os.path.dirname(__file__), 'test_image.png')

        # 画像をアップロード
        self.selenium.find_element(By.NAME, "image").send_keys(image_path)

        # 投稿ボタンをクリック
        self.selenium.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()

        # 画像が表示されることを確認
        container = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "tweet-image-container"))
        )
        image_element = container.find_element(By.CLASS_NAME, "tweet-image")
        self.assertTrue(image_element.is_displayed())

    def test_tweet_failure_empty(self):
        # 空の状態で投稿ボタンをクリック
        self.selenium.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()

        # エラーメッセージが表示されることを確認
        error_message = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )
        self.assertIn("テキストか画像のどちらかを投稿してください。", error_message.text)

    def test_tweet_failure_text_too_long(self):
        # maxlength属性を一時的に削除
        textarea = self.selenium.find_element(By.ID, "post-textarea")
        self.selenium.execute_script(
            "arguments[0].removeAttribute('maxlength');", textarea
        )

        # 141文字のテキストを入力
        long_text = "あ" * 141
        textarea.send_keys(long_text)

        # 投稿ボタンをクリック
        self.selenium.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()

        # エラーメッセージが表示されることを確認
        error_message = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )
        self.assertIn("この値は 140 文字以下でなければなりません( 141 文字になっています)。",
                      error_message.text)

    def test_tweet_success_text_and_image(self):
        # テキストを入力
        tweet_content = "画像付きツイートのテストです。"
        self.selenium.find_element(
            By.ID, "post-textarea").send_keys(tweet_content)

        # 画像をアップロード
        image_path = os.path.join(os.path.dirname(__file__), 'test_image.png')
        self.selenium.find_element(By.NAME, "image").send_keys(image_path)

        # 投稿ボタンをクリック
        self.selenium.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()

        # テキストと画像が表示されることを確認
        tweet_element = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="tweet-content"]'))
        )
        self.assertEqual(tweet_element.text, tweet_content)

        image_element = self.selenium.find_element(
            By.CLASS_NAME, "tweet-image")
        self.assertTrue(image_element.is_displayed())
