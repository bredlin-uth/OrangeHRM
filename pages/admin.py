import time

import allure
from selenium import webdriver
from selenium.webdriver.common.by import By

from generic_utils.Web_Utils import WebUtils
from pages.dashboard import DashboardPage


class LoginPage(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # self.driver = webdriver.Chrome()

    admin_txt = (By.XPATH, "//h6[text()='Admin']")
    add_btn = (By.XPATH, "//button[contains(.,'Add')]")
    user_role_dd = (By.XPATH, "//label[.='User Role']/../../descendant::div[@class='oxd-select-text-input']")
    status_dd = (By.XPATH, "//label[.='Status']/../../descendant::div[@class='oxd-select-text-input']")
    employee_name_tb = (By.XPATH, "//label[.='Employee Name']/../../descendant::input")
    username_tb = (By.XPATH, "//label[.='Username']/../../descendant::input")
    password_tb = (By.XPATH, "//label[.='Password']/../../descendant::input")
    confirm_password_tb = (By.XPATH, "//label[.='Confirm Password']/../../descendant::input")
    save_btn = (By.XPATH, "//button[contains(.,'Save')]")
    

    def top_bar_tab_menu(self, menu):
        return By.XPATH, f"//span[@class='oxd-topbar-body-nav-tab-item' and contains(.,'{menu}')]"

    def top_bar_tab_menu_items(self, item):
        return By.XPATH, f"//a[@class='oxd-topbar-body-nav-tab-link' and contains(.,'{item}')]"

    def dropdown_options(self, value):
        return By.XPATH, f"//div[@role='option']/span[.='{value}']"
