import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver

from generic_utils import Config_Utils


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")

@pytest.fixture()
def setup_and_teardown(request):
    global driver
    browser = request.config.getoption("--browser").lower()
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        driver = webdriver.Chrome(options)
    elif browser == "edge":
        driver = webdriver.Edge()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    else:
        raise Exception("Invalid browser.")

    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(Config_Utils.get_config("basic info", "url"))
    request.cls.driver = driver
    # yield
    # driver.quit()

@pytest.fixture()
def screenshot_on_failure(request):
    yield
    item = request.node
    if item.rep_call.failed:
        allure.attach(driver.get_screenshot_as_png(), name="failed_test", attachment_type=AttachmentType.PNG)

