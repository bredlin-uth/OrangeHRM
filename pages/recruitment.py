import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from generic_utils import Common_Utils
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
    success_message_toast = (By.XPATH, "//div[@class='oxd-toast-start']/descendant::p")
    firstname_tb = (By.NAME, "firstName")
    lastname_tb = (By.NAME, "lastName")

    def add_candidates_tb(self, title):
        return By.XPATH, f"//label[.='{title}']/../../descendant::input"

    def dropdown_options(self, value):
        return By.XPATH, f"//div[@role='option']/span[contains(.,'{value}')]"

    def select_date(self, date):
        split_date = Common_Utils.split_sentence(date)
        time.sleep(2)
        self.handle_form(self.form, self.year_cal).click()
        time.sleep(1)
        self.handle_form(self.form, self.select_option(split_date[2])).click()
        time.sleep(1)
        self.handle_form(self.form, self.month_cal).click()
        time.sleep(1)
        self.handle_form(self.form, self.select_option(split_date[1])).click()
        time.sleep(1)
        self.handle_form(self.form, self.date_cal(str(split_date[0]))).click()

    def verify_the_recruitment_page(self):
        status = self.check_element_is_displayed(self.recruitment_txt)
        self.attach_screenshot_in_allure("Navigated to the Recruitment page", "recruitment_page")
        return status

    def verify_the_success_toast(self):
        status = self.check_element_is_displayed(self.success_message_toast)
        return status

    # def add_candidate(self, name, vacancy, email, contact, keywords, date, notes):
    #     username = Common_Utils.split_sentence(name)
    #     self.handle_form(self.form, self.firstname_tb).send_keys(username[0])
    #     self.handle_form(self.form, self.lastname_tb).send_keys(username[1])
    #
    #     self.handle_form(self.form, self.).send_keys()
    #     self.handle_form(self.form, self.).send_keys()
    #     self.handle_form(self.form, self.).send_keys()
    #     self.handle_form(self.form, self.).send_keys()
    #
    #     self.handle_form(self.form, self.consent_to_keep_data_cb).click()
    #     self.handle_form(self.form, self.save_btn).click()


