import os
import time

import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By

from generic_utils import Common_Utils, Config_Utils
from generic_utils.Web_Utils import WebUtils


class RecruitmentPage(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # self.driver = webdriver.Chrome()

    recruitment_txt = (By.XPATH, "//h6[text()='Recruitment']")
    add_btn = (By.XPATH, "//button[contains(.,'Add')]")
    save_btn = (By.XPATH, "//button[contains(.,'Save')]")
    form = (By.XPATH, "//form[@class='oxd-form']")
    vacancy_dd = (By.XPATH, "//label[.='Vacancy']/../../descendant::div[@class='oxd-select-text-input']")
    date_of_application_cal = (By.XPATH, "//label[.='Date of Application']/../../descendant::input")
    notes_ta = (By.XPATH, "//label[.='Notes']/../../descendant::textarea")
    consent_to_keep_data_cb = (By.XPATH, "//input[@type='checkbox']")
    success_message_toast = (By.XPATH, "//div[@class='oxd-toast-start']/descendant::p[contains(@class, 'toast-message')]")
    firstname_tb = (By.NAME, "firstName")
    lastname_tb = (By.NAME, "lastName")
    applicant_name_txt = (By.XPATH, "//label[text()='Name']/../..//p")
    applicant_vacancy_txt = (By.XPATH, "//label[text()='Vacancy']/../..//p")
    download_icn = (By.XPATH, "//i[@class='oxd-icon bi-download']/..")

    month_cal = (By.XPATH, "//li[contains(@class,'oxd-calendar-selector-month')]/div")
    year_cal = (By.XPATH, "//li[contains(@class,'oxd-calendar-selector-year')]/div")

    def date_cal(self, date):
        return By.XPATH, f"//div[contains(@class,'oxd-calendar-date') and text()='{date}']"

    def select_option(self, option):
        return By.XPATH, f"//li[contains(@class,'oxd-calendar-dropdown--option') and contains(.,'{option}')]"

    def add_candidates_tb(self, title):
        return By.XPATH, f"//label[.='{title}']/../../descendant::input"

    def dropdown_options(self, value):
        return By.XPATH, f"//div[@role='option']/span[contains(.,'{value}')]"

    def select_date(self, date):
        split_date = Common_Utils.split_sentence(date)
        time.sleep(2)
        self.handle_form(self.form, self.year_cal).click()
        time.sleep(2)
        self.scroll_using_coordinates(300, -200)
        self.handle_form(self.form, self.select_option(split_date[2])).click()
        time.sleep(2)
        self.handle_form(self.form, self.month_cal).click()
        time.sleep(2)
        self.scroll_using_coordinates(300, -200)
        self.handle_form(self.form, self.select_option(split_date[1])).click()
        time.sleep(2)
        self.handle_form(self.form, self.date_cal(str(split_date[0]))).click()

    def verify_the_recruitment_page(self):
        status = self.check_element_is_displayed(self.recruitment_txt)
        with allure.step("Navigated to the Recruitment page"):
            allure.attach(self.driver.get_screenshot_as_png(), name="recruitment_page",
                          attachment_type=AttachmentType.PNG)
        return status

    def click_on_add_button(self):
        self.click_on_the_element(self.add_btn)

    def verify_the_success_toast(self):
        message = None
        try:
            self.check_element_is_displayed(self.success_message_toast)
            message = self.get_text_of_the_element(self.success_message_toast)
            print(message)
            return message
        except Exception:
            if message is None:
                print("Toast message not displayed")
                return "Toast message not displayed"

    def add_candidate(self, name, vacancy, email, contact, keywords, notes, file_path, date=None):
        username = Common_Utils.split_sentence(name)
        self.handle_form(self.form, self.firstname_tb).send_keys(username[0])
        self.handle_form(self.form, self.lastname_tb).send_keys(username[1])

        self.handle_form(self.form, self.vacancy_dd).click()
        self.handle_form(self.form, self.dropdown_options(vacancy)).click()

        self.handle_form(self.form, self.add_candidates_tb("Email")).send_keys(email)
        self.handle_form(self.form, self.add_candidates_tb("Contact Number")).send_keys(contact)
        self.handle_form(self.form, self.add_candidates_tb("Keywords")).send_keys(keywords)
        if date is not None:
            self.handle_form(self.form, self.select_date(date))
        # file = os.path.join(os.path.dirname(os.path.abspath('.')), file_path)
        file = os.path.join(os.path.abspath('.'), file_path)
        self.handle_form(self.form, self.add_candidates_tb("Resume")).send_keys(file)
        time.sleep(2)
        self.scroll_till_bottom_of_the_page()
        self.handle_form(self.form, self.notes_ta).send_keys(notes)
        with allure.step("Entered all the mandatory fields"):
            allure.attach(self.driver.get_screenshot_as_png(), name="add_candidate", attachment_type=AttachmentType.PNG)
        self.handle_form(self.form, self.save_btn).click()

    def verify_the_candidate_application(self, expected_name, expected_vacancy):
        actual_name = self.get_text_of_the_element(self.applicant_name_txt)
        actual_vacancy = self.get_text_of_the_element(self.applicant_vacancy_txt)
        if actual_name == expected_name:
            if actual_vacancy == expected_vacancy:
                return True
        with allure.step("Candidate Application"):
            allure.attach(self.driver.get_screenshot_as_png(), name="candidate_records",
                          attachment_type=AttachmentType.PNG)
        return False

    def download_candidate_resume(self):
        self.scroll_using_coordinates(800, 200)
        with allure.step("Candidates Records"):
            allure.attach(self.driver.get_screenshot_as_png(), name="candidates_record",
                          attachment_type=AttachmentType.PNG)
        self.wait_till_the_element_is_visible(self.download_icn)
        self.click_on_the_element(self.download_icn)
        time.sleep(5)
        return Common_Utils.get_recent_file(Config_Utils.get_config("directory info", "download_path"))
