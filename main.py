from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
from dotenv import load_dotenv

load_dotenv()

PROMISED_DOWN = 150
PROMISED_UP = 10
TWITTER_EMAIL = os.environ.get("TWITTER_EMAIL")
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")


class InternetSpeedTwitterBot:

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.down = None
        self.up = None

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        start_test = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a')
        start_test.click()
        time.sleep(90)
        self.down = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text
        self.up = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text

    def tweet_at_provider(self):
        self.driver.get('https://x.com/')
        time.sleep(5)
        try:
            close_welcome_message = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div[2]/div/div/div/button')
            close_welcome_message.click()
        except NoSuchElementException:
            pass

        sign_in = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[4]/a')
        sign_in.click()
        time.sleep(7)

        email_address = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')
        email_address.send_keys(TWITTER_EMAIL, Keys.ENTER)

        # Manual account verification may be needed.
        input("Press enter after verification:")
        time.sleep(7)

        password = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        password.send_keys(TWITTER_PASSWORD, Keys.ENTER)
        time.sleep(10)

        tweet = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div')
        if self.down < PROMISED_DOWN:
            tweet.send_keys(f"My internet up speed is {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up. Kindly fix.")
            # post_tweet = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button')
            # post_tweet.click()
        else:
            tweet.send_keys("My internet works fine. Thanks @my_isp")
            # post_tweet = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button')
            # post_tweet.click()
        self.driver.quit()


twitter_bot = InternetSpeedTwitterBot()
twitter_bot.get_internet_speed()
twitter_bot.tweet_at_provider()
