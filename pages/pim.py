import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from generic_utils.Web_Utils import WebUtils


class PimPage(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # self.driver = webdriver.Chrome()

    pim_txt = (By.XPATH, "//h6[text()='PIM']")
    help_icn = (By.XPATH, "//button[@title ='Help']")

    def verify_the_pim_page(self):
        status = self.check_element_is_displayed(self.pim_txt)
        self.attach_screenshot_in_allure("Navigated to the PIM page", "pim_page")
        return status

    def click_on_the_help_icon(self):
        self.click_on_the_element(self.help_icn)
        self.switch_between_tabs()
        self.attach_screenshot_in_allure("Navigated to the Help page", "help_page")
        self.switch_between_tabs()
