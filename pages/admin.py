import time

import allure
from selenium import webdriver
from selenium.webdriver.common.by import By

from generic_utils import Common_Utils
from generic_utils.Web_Utils import WebUtils
from pages.dashboard import DashboardPage


class AdminPage(WebUtils):
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
    form = (By.XPATH, "//form[@class='oxd-form']")
    success_message_toast = (By.XPATH, "//div[@class='oxd-toast-start']/descendant::p")
    username_txt = (By.XPATH, "(//div[@class='oxd-table-card']/div/div[2]/div)[2]")
    yes_delete_button = (By.XPATH, "//button[contains(.,'Yes, Delete')]")


    def top_bar_tab_menu(self, menu):
        return By.XPATH, f"//span[@class='oxd-topbar-body-nav-tab-item' and contains(.,'{menu}')]"

    def top_bar_tab_menu_items(self, item):
        return By.XPATH, f"//a[@class='oxd-topbar-body-nav-tab-link' and contains(.,'{item}')]"

    def dropdown_options(self, value):
        return By.XPATH, f"//div[@role='option']/span[contains(.,'{value}')]"

    def record_username(self, username):
        return By.XPATH, f"//div[@class='oxd-table-card']/descendant::div[.='{username}']"

    def select_checkbox(self, username):
        return By.XPATH, f"//div[.='{username}']/./preceding-sibling::div/descendant::input"

    def delete_icon(self, username):
        return By.XPATH, f"//div[.='{username}']/./following-sibling::div/descendant::i[@class='oxd-icon bi-trash']/.."

    def verify_the_admin_page(self):
        status = self.check_element_is_displayed(self.admin_txt)
        self.attach_screenshot_in_allure("Navigate to the Admin page", "navigated_to_admin_page")
        return status

    def select_users_from_the_dropdown(self, menu, item):
        self.click_on_the_element(self.top_bar_tab_menu(menu))
        self.wait_till_the_element_is_visible(self.top_bar_tab_menu_items(item))
        self.click_on_the_element(self.top_bar_tab_menu_items(item))

    def click_on_add_button(self):
        self.wait_till_the_element_is_visible(self.add_btn)
        self.click_on_the_element(self.add_btn)

    def add_user(self, user_role, status, employee_name, username, password):
        self.wait_till_the_element_is_visible(self.form)
        self.attach_screenshot_in_allure("Add User", "navigated_to_add_user")

        self.handle_form(self.form, self.user_role_dd).click()
        self.handle_form(self.form, self.dropdown_options(user_role)).click()
        self.handle_form(self.form, self.status_dd).click()
        self.handle_form(self.form, self.dropdown_options(status)).click()
        self.handle_form(self.form, self.employee_name_tb).send_keys(employee_name)
        self.handle_form(self.form, self.dropdown_options(employee_name)).click()
        username1 = username + str(Common_Utils.generate_random_number(5))
        self.handle_form(self.form, self.username_tb).send_keys(username1)
        self.handle_form(self.form, self.password_tb).send_keys(password)
        self.handle_form(self.form, self.confirm_password_tb).send_keys(password)
        self.handle_form(self.form, self.save_btn).click()
        return username1

    def verify_the_success_toast(self):
        status = self.check_element_is_displayed(self.success_message_toast)
        return status

    def verify_the_user_in_the_record(self, username):
        self.scroll_using_coordinates(0, 200)
        status = self.check_element_is_displayed(self.record_username(username))
        self.attach_screenshot_in_allure("Verify the user is in the record table", "added_record")
        return status

    def delete_user(self):
        self.scroll_till_element_is_visible(self.username_txt)
        username = self.get_text_of_the_element(self.username_txt)
        self.click_on_the_element(self.select_checkbox(username))
        self.click_on_the_element(self.delete_icon(username))
        self.wait_till_the_element_is_visible(self.yes_delete_button)
        self.attach_screenshot_in_allure("Delete User", "are_you_sure")
        self.click_on_the_element(self.yes_delete_button)
        return username

    def verify_the_user_is_deleted(self, username):
        self.scroll_till_bottom_of_the_page()
        status = self.is_element_not_displayed(self.record_username(username))
        self.attach_screenshot_in_allure("Delete User", "user_is_deleted")
        return status


