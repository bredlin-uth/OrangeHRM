import os

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver

from generic_utils import Config_Utils, Common_Utils, Excel_Utils

def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")

@pytest.fixture()
def setup_and_teardown(request):
    global driver
    browser = request.config.getoption("--browser").lower()
    timestamp = Common_Utils.get_timestamp()
    path = os.path.join(os.path.dirname(os.path.abspath('.')), Config_Utils.get_config("directory info", "download_folder"))
    download_path = Common_Utils.create_folder_with_timestamp(path, timestamp)
    Config_Utils.change_properties_file("directory info", "download_path", download_path)
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"download.default_directory": download_path})
        options.add_experimental_option('detach', False)
        driver = webdriver.Chrome(options)
    elif browser == "edge":
        driver = webdriver.Edge()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    else:
        raise Exception("Invalid browser.")

    driver.maximize_window()
    driver.implicitly_wait(10)
    url = Excel_Utils.fetch_data_from_excel("Credentials", "Testing", "URL")
    driver.get(url)
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.fixture()
def screenshot_on_failure(request):
    yield
    item = request.node
    if item.rep_call.failed:
        allure.attach(driver.get_screenshot_as_png(), name="failed_test", attachment_type=AttachmentType.PNG)
