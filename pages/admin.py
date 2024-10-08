import time

import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By

from generic_utils import Common_Utils
from generic_utils.Web_Utils import WebUtils


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
    success_message_toast = (By.XPATH, "//div[@class='oxd-toast-start']/descendant::p[contains(@class, 'toast-message')]")
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
        with allure.step("Navigate to the Admin page"):
            allure.attach(self.driver.get_screenshot_as_png(), name="admin_page", attachment_type=AttachmentType.PNG)
        self.log.info("Navigate to the Admin page")
        return status

    def select_users_from_the_dropdown(self, menu, item):
        self.click_on_the_element(self.top_bar_tab_menu(menu))
        self.log.info(f"Clicked on the {menu} menu")
        self.wait_till_the_element_is_visible(self.top_bar_tab_menu_items(item))
        self.click_on_the_element(self.top_bar_tab_menu_items(item))
        self.log.info(f"Clicked on the {item} item")
        with allure.step(f"Navigate to the {menu} page"):
            allure.attach(self.driver.get_screenshot_as_png(), name=f"{menu}_page", attachment_type=AttachmentType.PNG)
        self.log.info(f"Navigated to the {menu} page")

    def click_on_add_button(self):
        self.wait_till_the_element_is_visible(self.add_btn)
        self.click_on_the_element(self.add_btn)
        self.log.info(f"Clicked on the Add button")

    def add_user(self, user_role, status, employee_name, username, password):
        self.wait_till_the_element_is_visible(self.form)
        with allure.step("Add User"):
            allure.attach(self.driver.get_screenshot_as_png(), name="navigated_to_add_user", attachment_type=AttachmentType.PNG)

        self.handle_form(self.form, self.user_role_dd).click()
        self.handle_form(self.form, self.dropdown_options(user_role)).click()
        self.handle_form(self.form, self.status_dd).click()
        self.handle_form(self.form, self.dropdown_options(status)).click()
        self.handle_form(self.form, self.employee_name_tb).send_keys(employee_name)
        self.wait_till_the_element_visible(self.handle_form(self.form, self.dropdown_options(employee_name))).click()
        username1 = username + str(Common_Utils.generate_random_number(5))
        self.handle_form(self.form, self.username_tb).send_keys(username1)
        self.handle_form(self.form, self.password_tb).send_keys(password)
        self.handle_form(self.form, self.confirm_password_tb).send_keys(password)
        with allure.step("Entered the field for the add user "):
            allure.attach(self.driver.get_screenshot_as_png(), name="add_user", attachment_type=AttachmentType.PNG)
        self.log.info("Entered all the mandatory fields")
        self.handle_form(self.form, self.save_btn).click()
        self.log.info("Clicked on the Save button")
        return username1

    def verify_the_success_toast(self):
        message = None
        try:
            self.check_element_is_displayed(self.success_message_toast)
            message = self.get_text_of_the_element(self.success_message_toast)
            self.log.info(f"{message} toast message is displayed")
            return message
        except Exception:
            if message is None:
                self.log.warn("Toast message is not displayed")
                return "Toast message is not displayed"

    def verify_the_user_in_the_record(self, username):
        self.scroll_using_coordinates(0, 200)
        status = self.check_element_is_displayed(self.record_username(username))
        with allure.step("User Records"):
            allure.attach(self.driver.get_screenshot_as_png(), name="user_records", attachment_type=AttachmentType.PNG)
        self.log.info("Verified the user in the record")
        return status

    def delete_user(self, username):
        self.scroll_till_element_is_visible(self.select_checkbox(username))
        time.sleep(1)
        self.click_on_the_element(self.select_checkbox(username))
        self.click_on_the_element(self.delete_icon(username))
        self.log.info(f"Clicked on the Delete Icon for the {username} user")
        self.wait_till_the_element_is_visible(self.yes_delete_button)
        with allure.step("Delete Popup"):
            allure.attach(self.driver.get_screenshot_as_png(), name="are_you_sure", attachment_type=AttachmentType.PNG)
        self.click_on_the_element(self.yes_delete_button)
        self.log.info("Clicked on the Yes Delete button")
        return username

    def verify_the_user_is_deleted(self, username):
        self.scroll_till_bottom_of_the_page()
        status = self.is_element_not_displayed(self.record_username(username))
        with allure.step("User Records after Deleting"):
            allure.attach(self.driver.get_screenshot_as_png(), name="records_after_deletion", attachment_type=AttachmentType.PNG)
        self.log.info(f"After Deleting {username} from the record is deleted")
        return status


