from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")

def setup_and_teardown(request):
    global driver
    browser = request.config.getoption("--browser").lower()
    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "edge":
        driver = webdriver.Edge()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    else:
        raise Exception("Invalid browser.")