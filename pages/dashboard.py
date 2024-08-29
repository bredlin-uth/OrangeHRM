import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from generic_utils.Web_Utils import WebUtils


class DashboardPage(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # self.driver = webdriver.Chrome()

    dashboard_txt = (By.XPATH, "//h6[text()='Dashboard']")
    search_tb = (By.XPATH, "//div[@class='oxd-main-menu-search']/input")

    def menu_item_lnk(self, name):
        return By.XPATH, f"//ul[@class='oxd-main-menu']/descendant::span[contains(.,'{name}')]"

    def verify_the_dashboard_page(self):
        status = self.check_element_is_displayed(self.dashboard_txt)
        self.attach_screenshot_in_allure("Login to the application", "login_successfully")
        return status

    def click_on_menu_item(self, menu):
        self.click_on_the_element(self.menu_item_lnk(menu))
        time.sleep(2)
        self.attach_screenshot_in_allure(f"Navigate to the {menu} page", f"navigated_to_{menu}_page")

