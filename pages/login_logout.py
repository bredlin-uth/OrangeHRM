from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    username_tb = (By.NAME, "username")
    password_tb = (By.NAME, "password")
    login_btn = (By.XPATH, "//button[contains(@class, 'login-button')]")

    user_dd = (By.XPATH, "//p[@class='oxd-userdropdown-name']")
    logout_opt = (By.XPATH, "//li/a[text()='Logout']")

    def login_to_the_application(self, username, password):
        self.driver.find_element(*self.username_tb).send_keys(username)
        self.driver.find_element(*self.password_tb).send_keys(password)
        self.driver.find_element(*self.login_btn).click()

    def logout_from_the_application(self):
        self.driver.find_element(*self.user_dd).click()
        self.driver.find_element(*self.logout_opt).click()

