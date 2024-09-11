import os

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver

from generic_utils import Excel_Utils, Config_Utils, Common_Utils


@pytest.fixture(scope='session')
def download_dir():
    timestamp = Common_Utils.get_timestamp()
    print(timestamp)
    # download_path = os.path.join(os.path.dirname(os.path.abspath('.')), Config_Utils.get_config("directory info", "download_folder"))
    # excel_path = os.path.join(os.path.dirname(os.path.abspath('.')), Config_Utils.get_config("directory info", "excel_output"))
    download_path = os.path.join(os.path.abspath('.'),
                                 Config_Utils.get_config("directory info", "download_folder"))
    excel_path = os.path.join(os.path.abspath('.'),
                              Config_Utils.get_config("directory info", "excel_output"))

    download_directory = Common_Utils.create_folder_with_timestamp(download_path, timestamp)
    excel_dir = Common_Utils.create_folder_with_timestamp(excel_path, timestamp)
    excel_directory = Excel_Utils.create_a_excel_file(os.path.join(excel_dir, "Excel_Report.xlsx"))
    exc = 0
    if exc == 0:
        Config_Utils.change_properties_file("directory info", "download_path", download_directory)
        Config_Utils.change_properties_file("directory info", "excel_path", excel_directory)
        exc += 1
    return download_directory


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")


@pytest.fixture()
def setup_and_teardown(request, download_dir):
    global driver
    browser = request.config.getoption("--browser").lower()
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
            'download.default_directory': download_dir,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True
        })
        options.add_experimental_option('detach', False)
        driver = webdriver.Chrome(options)
    elif browser == "edge":
        driver = webdriver.Edge()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    else:
        raise Exception("Invalid browser.")

    driver.maximize_window()
    driver.implicitly_wait(15)
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

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep
