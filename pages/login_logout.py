import time

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

    def verify_the_login_page(self):
        return self.check_element_is_displayed(self.login_txt)

    def login_to_the_application(self, username, password):
        self.set_value_to_the_textfield(self.username_tb, username)
        self.set_value_to_the_textfield(self.password_tb, password)
        self.click_on_the_element(self.login_btn)
        return DashboardPage(self.driver)

    def logout_from_the_application(self):
        self.click_on_the_element(self.user_dd)
        self.click_on_the_element(self.logout_opt)
        time.sleep(2)
        self.attach_screenshot_in_allure("Logout from the application", "logout_successfully")
