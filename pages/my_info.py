import os
import time

import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By

from generic_utils import Common_Utils, Excel_Utils, Config_Utils
from generic_utils.Web_Utils import WebUtils


class MyInfoPage(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # self.driver = webdriver.Chrome()

    personal_details_txt = (By.XPATH, "//h6[text()='Personal Details']")
    save1_btn = (By.XPATH, "(//button[contains(.,'Save')])[1]")
    save3_btn = (By.XPATH, "(//button[contains(.,'Save')])[3]")
    form1 = (By.XPATH, "(//form[@class='oxd-form'])[1]")
    form3 = (By.XPATH, "(//form[@class='oxd-form'])[3]")
    nationality_dd = (By.XPATH, "//label[.='Nationality']/../../descendant::div[@class='oxd-select-text-input']")
    marital_status_dd = (By.XPATH, "//label[.='Marital Status']/../../descendant::div[@class='oxd-select-text-input']")
    date_of_birth_cal = (By.XPATH, "//label[.='Date of Birth']/../../descendant::input")
    license_expiry_date_cal = (By.XPATH, "//label[.='License Expiry Date']/../../descendant::input")

    success_message_toast = (By.XPATH, "//div[@class='oxd-toast-start']/descendant::p[contains(@class, 'toast-message')]")
    firstname_tb = (By.NAME, "firstName")
    lastname_tb = (By.NAME, "lastName")
    month_cal = (By.XPATH, "//li[contains(@class,'oxd-calendar-selector-month')]/div")
    year_cal = (By.XPATH, "//li[contains(@class,'oxd-calendar-selector-year')]/div")
    add_btn = (By.XPATH, "//button[contains(.,'Add')]")

    def personal_details_tb(self, title):
        return By.XPATH, f"//label[contains(.,'{title}')]/../../descendant::input"

    def date_cal(self, date):
        return By.XPATH, f"//div[contains(@class,'oxd-calendar-date') and text()='{date}']"

    def select_option(self, option):
        return By.XPATH, f"//li[contains(@class,'oxd-calendar-dropdown--option') and contains(.,'{option}')]"

    def dropdown_options(self, value):
        return By.XPATH, f"//div[@role='option']/span[contains(.,'{value}')]"

    def gender_rb(self, value):
        return By.XPATH, f"//label[.='Gender']/../../descendant::label[text()='{value}']/.."

    def download_icon(self, file_name):
        return By.XPATH, f"//div[text()='{file_name}']/../../descendant::i[@class='oxd-icon bi-download']/.."

    def select_date(self, date):
        split_date = Common_Utils.split_sentence(date)
        time.sleep(2)
        self.wait_till_the_element_visible(self.handle_form(self.form1, self.year_cal)).click()
        time.sleep(2)
        self.scroll_using_coordinates(300, -100)
        self.wait_till_the_element_visible(self.handle_form(self.form1, self.select_option(split_date[2]))).click()
        time.sleep(2)
        self.wait_till_the_element_visible(self.handle_form(self.form1, self.month_cal)).click()
        time.sleep(2)
        self.scroll_using_coordinates(300, -100)
        self.wait_till_the_element_visible(self.handle_form(self.form1, self.select_option(split_date[1]))).click()
        time.sleep(2)
        self.scroll_using_coordinates(0, 0)
        self.wait_till_the_element_visible(self.handle_form(self.form1, self.date_cal(str(split_date[0])))).click()

    def verify_the_info_page(self):
        status = self.check_element_is_displayed(self.personal_details_txt)
        with allure.step("Navigated to the My Info page"):
            allure.attach(self.driver.get_screenshot_as_png(), name="my_info_page", attachment_type=AttachmentType.PNG)
        return status

    def verify_the_success_toast(self):
        message = None
        try:
            self.check_element_is_displayed(self.success_message_toast)
            message = self.get_text_of_the_element(self.success_message_toast)
            return message
        except Exception:
            if message is None:
                return "Toast message not displayed"

    def add_personal_details(self, name, employee_id, other_id, licence_number, expiry_date, nationality, marital_status, dob, gender):
        username = Common_Utils.split_sentence(name)

        self.clear_and_enter(self.firstname_tb, username[0])
        self.clear_and_enter(self.lastname_tb, username[1])
        self.clear_and_enter(self.personal_details_tb("Employee Id"), employee_id)
        self.clear_and_enter(self.personal_details_tb("Other Id"), other_id)
        self.clear_and_enter(self.personal_details_tb("License Number"), licence_number)
        self.handle_form(self.form1, self.license_expiry_date_cal).click()
        self.select_date(expiry_date)
        self.scroll_using_coordinates(0, 0)
        self.handle_form(self.form1, self.date_of_birth_cal).click()
        self.scroll_using_coordinates(300, 0)
        self.select_date(dob)
        self.scroll_using_coordinates(0, 0)
        self.handle_form(self.form1, self.nationality_dd).click()
        time.sleep(2)
        self.handle_form(self.form1, self.dropdown_options(nationality)).click()
        self.handle_form(self.form1, self.marital_status_dd).click()
        self.handle_form(self.form1, self.dropdown_options(marital_status)).click()

        self.handle_form(self.form1, self.gender_rb(gender)).click()
        with allure.step("Entered all the mandatory fields"):
            allure.attach(self.driver.get_screenshot_as_png(), name="personal_details", attachment_type=AttachmentType.PNG)
        self.handle_form(self.form1, self.save1_btn).click()

    def verify_the_profile_record(self):
        self.click_on_the_element(self.add_btn)
        # file_path = os.path.join(os.path.dirname(os.path.abspath('.')), Config_Utils.get_config("directory info", "sample_file"))
        file_path = os.path.join(os.path.abspath('.'), Config_Utils.get_config("directory info", "sample_file"))
        expected_data = Excel_Utils.get_row_excel_data("Sheet1", 1, file_path)
        time.sleep(2)
        self.scroll_using_coordinates(300, 300)
        self.handle_form(self.form3, self.personal_details_tb("Select File")).send_keys(file_path)
        self.handle_form(self.form3, self.save3_btn).click()
        with allure.step("Profile Records"):
            allure.attach(self.driver.get_screenshot_as_png(), name="profile_records", attachment_type=AttachmentType.PNG)
        file_name = Common_Utils.split_sentence(file_path, "\\")
        self.click_on_the_element(self.download_icon(file_name[-1]))
        time.sleep(10)
        downloaded_file = os.path.join(Config_Utils.get_config("directory info", "download_path"), file_name[-1])
        actual_data = Excel_Utils.get_row_excel_data("Sheet1", 1, downloaded_file)
        return expected_data == actual_data
