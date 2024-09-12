import time

import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By

from generic_utils.Web_Utils import WebUtils
from pages.dashboard import DashboardPage


class LoginPage(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    login_txt = (By.XPATH, "//h5[text()='Login']")
    username_tb = (By.NAME, "username")
    password_tb = (By.NAME, "password")
    login_btn = (By.XPATH, "//button[contains(@class, 'login-button')]")

    user_dd = (By.XPATH, "//p[@class='oxd-userdropdown-name']")
    logout_opt = (By.XPATH, "//li/a[text()='Logout']")

    def take_screenshot(self, name):
        screenshot_path = f"{name}.png"
        self.driver.save_screenshot(screenshot_path)
        self.log.info(f'Screenshot saved: {screenshot_path}')
        return screenshot_path

    def verify_the_login_page(self):
        time.sleep(1)
        status = self.check_element_is_displayed(self.login_txt)
        self.log.info("Navigated to the Login Page")
        with allure.step("Navigated to the Login page"):
            allure.attach(self.driver.get_screenshot_as_png(), name="login_page", attachment_type=AttachmentType.PNG)
        return status

    def login_to_the_application(self, username, password):
        self.set_value_to_the_textfield(self.username_tb, username)
        self.set_value_to_the_textfield(self.password_tb, password)
        self.log.info("Entered username and password")
        with allure.step("Entered all the mandatory field"):
            allure.attach(self.driver.get_screenshot_as_png(), name="login", attachment_type=AttachmentType.PNG)
        self.click_on_the_element(self.login_btn)
        self.log.info("Clicked on the Login button")
        return DashboardPage(self.driver)

    def logout_from_the_application(self):
        self.click_on_the_element(self.user_dd)
        self.log.info("Clicked on the User Dropdown")
        self.click_on_the_element(self.logout_opt)
        self.log.info("Clicked on the Logout option")
        time.sleep(2)
        with allure.step("Navigated to the Login page"):
            allure.attach(self.driver.get_screenshot_as_png(), name="login_page", attachment_type=AttachmentType.PNG)
        self.log.info("Successfully Logged out from the application")
