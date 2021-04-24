import json

from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import os


class Linkedin:
    """
    Purpose:
    1. Login to the browser and maintain a session
    2. Function to take input as url of a linkedin user, user must be connected to the logined account
    3. Function to send the message to the user, message could be dynamic
    """
    session = None

    @classmethod
    def get_browser(cls, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        else:
            pass
        options.add_argument("--start-maximized")
        options.add_argument("user-agent=DN")
        options.add_extension('packetstream_us.zip')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Linux64",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        return driver

    @classmethod
    def login(cls, username, password):
        """
        :param username: Linkedin username
        :param password: Linkedin password
        :return: Linkedin instance
        """

        driver = Linkedin.get_browser(headless=False)
        print('Driver initialized successfully!')
        driver.get('https://www.linkedin.com/')
        if not os.path.exists(f'{username}.json'):
            username_login = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="username"]')))
            for i in username:
                time.sleep(random.random() / 10)
                username_login.send_keys(i)
            password_login = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="current-password"]')))
            for i in password:
                time.sleep(random.random() / 10)
                password_login.send_keys(i)
            signin_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@class="sign-in-form__submit-button"]')))
            signin_button.click()
            print('Login Successfull!')
            with open(f'{username}.json', 'w') as f:
                f.write(json.dumps(driver.get_cookies()))
        else:
            driver.delete_all_cookies()
            for i in json.load(open(f'{username}.json')):
                driver.add_cookie(i)
            driver.refresh()
            time.sleep(10)
            print('Login Successfull using existing cookies!')

        Linkedin.session = driver
        return cls(username, password)

    @staticmethod
    def send_message(message):
        """
        :param message: that is to be send to the targeted user
        :return: None
        """
        if type(message) != str:
            raise ValueError('message must be a string')

        Linkedin.session.get(
            "https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH")
        # find the number of connections and generate no of iteration required
        raw_r = WebDriverWait(Linkedin.session, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="search-results-container"]/div[1]')))

        while True:
            buttons = WebDriverWait(Linkedin.session, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, '//li[@class="reusable-search__result-container "]//button')))

            for button in buttons:

                time.sleep(2)
                button.click()
                time.sleep(random.randrange(10, 55))

                # type in the message
                type_message = WebDriverWait(Linkedin.session, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//div[contains(@class, "msg-form__contenteditable")]/p')))
                type_message.click()
                for i in message:
                    time.sleep(random.random() / 10)
                    type_message.send_keys(i)
                submit = WebDriverWait(Linkedin.session, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "msg-form__send-button ")]')))
                submit.click()
                time.sleep(2)

                # close the hovered conversation box
                message_button = WebDriverWait(Linkedin.session, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "msg-overlay-conversation-bubble")]/header/section[2]/button[2]')))
                message_button.click()

            next_button = WebDriverWait(Linkedin.session, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Next"]')))
            # click the next button if its clickable
            if bool(next_button.get_attribute('disabled')):
                break

            next_button.click()

        print(f'Message sent successfully')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        pass
