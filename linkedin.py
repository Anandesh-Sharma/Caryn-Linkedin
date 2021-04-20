from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions
import math
import time
import random


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
        options.add_argument("window-size=1920,1080")
        options.add_argument("user-agent=DN")
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
        username_login = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="username"]')))
        username_login.send_keys(username)
        password_login = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="current-password"]')))
        password_login.send_keys(password)
        signin_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="sign-in-form__submit-button"]')))
        signin_button.click()
        print('Login Successfull!')
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
        r = raw_r.text.split(' ')[0]
        # TODO can we have this case 1,000 ? if so; needs to be done
        r = math.ceil(int(r) / 10)
        first_page = True
        for i in range(r):
            if first_page:
                first_page = False
                pass
            else:
                Linkedin.session.get(
                    f'https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH&page={i + 1}')
            buttons = WebDriverWait(Linkedin.session, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, '//li[@class="reusable-search__result-container "]//button')))

            for button in buttons:

                time.sleep(2)
                button.click()
                time.sleep(random.randrange(0, 15))

                # type in the message
                type_message = WebDriverWait(Linkedin.session, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//div[contains(@class, "msg-form__contenteditable")]/p')))
                type_message.click()
                type_message.send_keys(message)
                submit = WebDriverWait(Linkedin.session, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "msg-form__send-button ")]')))
                submit.click()
                time.sleep(2)

                # close the hovered conversation box
                message_button = WebDriverWait(Linkedin.session, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "msg-overlay-conversation-bubble")]/header/section[2]/button[2]')))
                message_button.click()
        print(f'Message sent successfully to {r} connected persons')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        pass
