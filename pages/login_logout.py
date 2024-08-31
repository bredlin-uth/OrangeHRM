import time

import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By

from generic_utils import Excel_Utils
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

    def verify_the_login_page(self):
        status = self.check_element_is_displayed(self.login_txt)
        with allure.step("Navigated to the Login page"):
            allure.attach(self.driver.get_screenshot_as_png(), name="login_page", attachment_type=AttachmentType.PNG)
        return status

    def login_to_the_application(self):
        username = Excel_Utils.fetch_data_from_excel("Credentials", "Testing", "Username")
        password = Excel_Utils.fetch_data_from_excel("Credentials", "Testing", "Password")
        self.set_value_to_the_textfield(self.username_tb, username)
        self.set_value_to_the_textfield(self.password_tb, password)
        with allure.step("Entered all the mandatory field"):
            allure.attach(self.driver.get_screenshot_as_png(), name="login", attachment_type=AttachmentType.PNG)
        self.click_on_the_element(self.login_btn)
        return DashboardPage(self.driver)

    def logout_from_the_application(self):
        self.click_on_the_element(self.user_dd)
        self.click_on_the_element(self.logout_opt)
        time.sleep(2)
        with allure.step("Navigated to the Login page"):
            allure.attach(self.driver.get_screenshot_as_png(), name="login_page", attachment_type=AttachmentType.PNG)
