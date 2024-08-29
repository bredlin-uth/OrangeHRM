import time

import pytest

from generic_utils import Config_Utils
from pages.dashboard import DashboardPage
from pages.login_logout import LoginPage


@pytest.mark.usefixtures("setup_and_teardown")
class Test_T001_Login:
    def test_login(self):
        login_page = LoginPage(self.driver)
        assert login_page.verify_the_login_page()
        username = Config_Utils.get_config("credential info", "username")
        password = Config_Utils.get_config("credential info", "password")
        dashboard_page = login_page.login_to_the_application(username, password)
        assert dashboard_page.verify_the_dashboard_page()
