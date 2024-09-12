import time

import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By

from generic_utils import Common_Utils
from generic_utils.Web_Utils import WebUtils


class LeavePage(WebUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # self.driver = webdriver.Chrome()

    leave_txt = (By.XPATH, "//h6[text()='Leave']")
    apply_tab = (By.XPATH, "//li/a[@class='oxd-topbar-body-nav-tab-item' and .='Apply']")
    my_leave_tab = (By.XPATH, "//li/a[@class='oxd-topbar-body-nav-tab-item' and .='My Leave']")
    leave_type_dd = (By.XPATH, "//label[.='Leave Type']/../../descendant::div[@class='oxd-select-text-input']")
    duration_dd = (By.XPATH, "//label[.='Duration']/../../descendant::div[@class='oxd-select-text-input']")
    from_date_cal = (By.XPATH, "//label[.='From Date']/../../descendant::input")
    to_date_cal = (By.XPATH, "//label[.='To Date']/../../descendant::input")
    comments_ta = (By.XPATH, "//label[.='Comments']/../../descendant::textarea")
    apply_btn = (By.XPATH, "//button[@type='submit']")
    form = (By.XPATH, "//form[@class='oxd-form']")
    month_cal = (By.XPATH, "//li[contains(@class,'oxd-calendar-selector-month')]/div")
    year_cal = (By.XPATH, "//li[contains(@class,'oxd-calendar-selector-year')]/div")
    success_message_toast = (By.XPATH, "//div[@class='oxd-toast-start']/descendant::p[contains(@class, 'toast-message')]")

    def dropdown_options(self, value):
        return By.XPATH, f"//div[@role='option']/span[contains(.,'{value}')]"

    def date_cal(self, date):
        return By.XPATH, f"//div[contains(@class,'oxd-calendar-date') and text()='{date}']"

    def select_option(self, option):
        return By.XPATH, f"//li[contains(@class,'oxd-calendar-dropdown--option') and contains(.,'{option}')]"

    def table_record(self, text):
        return By.XPATH, f"//div[@class='oxd-table-card']/descendant::div[text()='{text}']"

    def verify_the_leave_page(self):
        status = self.check_element_is_displayed(self.leave_txt)
        with allure.step("Navigated to the Leave page"):
            allure.attach(self.driver.get_screenshot_as_png(), name="leave_page",attachment_type=AttachmentType.PNG)
        self.log.info("Navigated to the Leave page")
        return status

    def click_on_apply_tab(self):
        self.click_on_the_element(self.apply_tab)
        self.log.info("Clicked on the Apply tab")
        time.sleep(2)
        with allure.step("Navigated to the Apply page"):
            allure.attach(self.driver.get_screenshot_as_png(), name="apply_page", attachment_type=AttachmentType.PNG)
        self.log.info("Navigated to the Apply page")

    def select_date(self, date):
        split_date = Common_Utils.split_sentence(date)
        time.sleep(2)
        self.wait_till_the_element_visible(self.handle_form(self.form, self.year_cal)).click()
        time.sleep(2)
        self.scroll_using_coordinates(300, -200)
        self.wait_till_the_element_visible(self.handle_form(self.form, self.select_option(split_date[2]))).click()
        time.sleep(2)
        self.wait_till_the_element_visible(self.handle_form(self.form, self.month_cal)).click()
        time.sleep(2)
        self.scroll_using_coordinates(300, -200)
        self.wait_till_the_element_visible(self.handle_form(self.form, self.select_option(split_date[1]))).click()
        time.sleep(2)
        self.scroll_using_coordinates(0, 0)
        self.wait_till_the_element_visible(self.handle_form(self.form, self.date_cal(str(split_date[0])))).click()
        self.log.info("Selected the date")

    def apply_leave(self, leave_type, from_date, to_date, comments):
        self.handle_form(self.form, self.leave_type_dd).click()
        self.handle_form(self.form, self.dropdown_options(leave_type)).click()
        self.handle_form(self.form, self.from_date_cal).click()
        self.select_date(from_date)
        self.handle_form(self.form, self.to_date_cal).click()
        self.select_date(to_date)
        self.handle_form(self.form, self.comments_ta).send_keys(comments)
        with allure.step("Entered all the leave fields"):
            allure.attach(self.driver.get_screenshot_as_png(), name="apply_leave", attachment_type=AttachmentType.PNG)
        self.log.info("Entered all the mandatory fields")
        self.handle_form(self.form, self.apply_btn).click()
        self.log.info("Click on the Apply button")

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

    def click_on_my_leave_tab(self):
        self.click_on_the_element(self.my_leave_tab)
        self.log.info("Clicked on the Leave tab")
        self.scroll_till_bottom_of_the_page()
        with allure.step("Navigated to the My Leave page"):
            allure.attach(self.driver.get_screenshot_as_png(), name="my_leave_page", attachment_type=AttachmentType.PNG)
        self.log.info("Navigated to the My Leave page")

    def verify_the_applied_leave(self, leave_type, comments):
        status = self.check_element_is_displayed(self.table_record(leave_type)) and self.check_element_is_displayed(self.table_record(comments))
        with allure.step("Applied leave Records"):
            allure.attach(self.driver.get_screenshot_as_png(), name="leave_records", attachment_type=AttachmentType.PNG)
        self.log.info("Applied leave is in the record")
        return status



