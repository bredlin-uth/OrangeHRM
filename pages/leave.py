import time

from selenium import webdriver
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
    month_cal = (By.XPATH, "//li[@class='oxd-calendar-selector-month']/div")
    year_cal = (By.XPATH, "//li[@class='oxd-calendar-selector-year']/div")
    success_message_toast = (By.XPATH, "//div[@class='oxd-toast-start']/descendant::p")

    def dropdown_options(self, value):
        return By.XPATH, f"//div[@role='option']/span[contains(.,'{value}')]"

    def date_cal(self, date):
        return By.XPATH, f"//div[@class='oxd-calendar-date' and text()='{date}']"

    def select_option(self, option):
        return By.XPATH, f"//li[contains(@class,'oxd-calendar-dropdown--option') and contains(.,'{option}')]"

    def table_record(self, text):
        return By.XPATH, f"//div[@class='oxd-table-card']/descendant::div[text()='{text}']"

    def verify_the_leave_page(self):
        status = self.check_element_is_displayed(self.leave_txt)
        self.attach_screenshot_in_allure("Navigated to the Leave page", "leave_page")
        return status

    def click_on_apply_tab(self):
        self.click_on_the_element(self.apply_tab)
        time.sleep(2)
        self.attach_screenshot_in_allure("Navigate to the apply leave page", "apply_leave_page")

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

    def apply_leave(self, leave_type, from_date, to_date, comments):
        self.handle_form(self.form, self.leave_type_dd).click()
        self.handle_form(self.form, self.dropdown_options(leave_type)).click()
        self.handle_form(self.form, self.from_date_cal).click()
        self.select_date(from_date)
        self.handle_form(self.form, self.to_date_cal).click()
        self.select_date(to_date)
        self.handle_form(self.form, self.comments_ta).send_keys(comments)
        self.handle_form(self.form, self.apply_btn).click()

    def verify_the_success_toast(self):
        status = self.check_element_is_displayed(self.success_message_toast)
        return status

    def click_on_my_leave_tab(self):
        self.click_on_the_element(self.my_leave_tab)
        self.scroll_till_bottom_of_the_page()
        self.attach_screenshot_in_allure("Navigate to the my leave page", "my_leave_page")

    def verify_the_applied_leave(self, leave_type, comments):
        return self.check_element_is_displayed(self.table_record(leave_type)) and self.check_element_is_displayed(self.table_record(comments))




