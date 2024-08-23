from selenium.webdriver.common.by import By


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    username_tb = (By.NAME, "username")
    password_tb = (By.NAME, "password")
    login_btn = (By.XPATH, "//button[contains(@class, 'login-button')]")

    def login_to_the_application(self):
        pass


