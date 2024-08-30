import time

import allure
from allure_commons.types import AttachmentType
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
    help_center_img = (By.XPATH, "//a/img[@alt='OrangeHRM Help Center home page']")

    def verify_the_pim_page(self):
        status = self.check_element_is_displayed(self.pim_txt)
        with allure.step("Navigated to the PIM page"):
            allure.attach(self.driver.get_screenshot_as_png(), name="pim_page", attachment_type=AttachmentType.PNG)
        return status

    def verify_orange_hrm_help(self,url):
        self.click_on_the_element(self.help_icn)
        self.switch_between_tabs()
        self.verify_the_url(url)
        self.check_element_is_displayed(self.help_center_img)
        with allure.step("Navigated to the Help page"):
            allure.attach(self.driver.get_screenshot_as_png(), name="help_page", attachment_type=AttachmentType.PNG)
        self.switch_between_tabs()
        with allure.step("Navigated back to the old tab"):
            allure.attach(self.driver.get_screenshot_as_png(), name="old_tab", attachment_type=AttachmentType.PNG)
