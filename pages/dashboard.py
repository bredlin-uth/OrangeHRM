import time

import allure
from allure_commons.types import AttachmentType
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
    employee_distribution_canvas = (By.XPATH, "//p[text()='Employee Distribution by Sub Unit']/ancestor::div[contains(@class,'oxd-sheet--rounded')]/descendant::canvas")
    tool_tip = (By.ID, "oxd-pie-chart-tooltip")

    def menu_item_lnk(self, name):
        return By.XPATH, f"//ul[@class='oxd-main-menu']/descendant::span[contains(.,'{name}')]"

    def verify_the_dashboard_page(self):
        status = self.check_element_is_displayed(self.dashboard_txt)
        with allure.step("Navigated to the Dashboard page"):
            allure.attach(self.driver.get_screenshot_as_png(), name="dashboard_page", attachment_type=AttachmentType.PNG)
        return status

    def click_on_menu_item(self, menu):
        self.click_on_the_element(self.menu_item_lnk(menu))
        time.sleep(2)
        
    def extract_data_from_canvas(self):
        time.sleep(2)
        self.scroll_using_coordinates(0, 250)
        self.mouse_over_on_the_element(self.employee_distribution_canvas, 50, 50)
        self.wait_till_the_element_is_visible(self.tool_tip)
        with allure.step("Pie Chart"):
            allure.attach(self.driver.get_screenshot_as_png(), name="canvas_data", attachment_type=AttachmentType.PNG)
        return self.get_text_of_the_element(self.tool_tip)
