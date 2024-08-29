import time

import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import ElementClickInterceptedException, NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebUtils:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        # driver = webdriver.Chrome()

    def click_on_the_element(self, element):
        try:
            self.driver.find_element(*element).click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(*element))

    def set_value_to_the_textfield(self, element, value):
        try:
            self.driver.find_element(*element).click()
            self.driver.find_element(*element).clear()
            self.driver.find_element(*element).send_keys(value)
        except Exception:
            self.driver.executeScript(f"arguments[0].value='{value}';", *element);

    def check_element_is_displayed(self, element):
        try:
            element = self.wait.until(
                EC.presence_of_element_located(element))
            return element.is_displayed()
        except Exception as e:
            print(f"Element not displayed: {e}")
            return False

    def wait_till_the_element_is_visible(self, element):
        try:
            element = self.wait.until(
                EC.visibility_of_element_located(element))
        except Exception as e:
            print(f"Element is not visible: {e}")

    def attach_screenshot_in_allure(self, step_name, file_name):
        with allure.step(step_name):
            allure.attach(self.driver.get_screenshot_as_png(), name=file_name, attachment_type=AttachmentType.PNG)

    def handle_form(self, form_element, element):
        form = self.wait.until(EC.visibility_of_element_located(form_element))
        return form.find_element(*element)

    def scroll_using_coordinates(self, x, y):
        self.driver.execute_script(f"window.scrollTo({int(x)}, {int(y)});")

    def scroll_till_bottom_of_the_page(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(1)

    def scroll_till_element_is_visible(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.driver.find_element(*element))
        time.sleep(1)

    def get_text_of_the_element(self, element):
        return self.driver.find_element(*element).text

    def is_element_not_displayed(self, element):
        try:
            element = self.driver.find_element(*element)
            return not element.is_displayed()
        except (NoSuchElementException, ElementNotVisibleException):
            return True

    def switch_to_tab_by_title(self, title):
        self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//title[contains(text(), '{}')]".format(title))))

        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if title in self.driver.title:
                break

    def switch_to_tab_by_index(self, index):
        handles = self.driver.window_handles
        if 0 <= index < len(handles):
            self.driver.switch_to.window(handles[index])
        else:
            print("Invalid tab index.")

    def switch_between_tabs(self):
        handles = self.driver.window_handles
        current_handle = self.driver.current_window_handle
        for handle in handles:
            if not (handle == current_handle):
                self.driver.switch_to.window(handle)
