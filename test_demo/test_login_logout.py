import allure
import pytest

from generic_utils import Excel_Utils, Config_Utils
from pages.login_logout import LoginPage
from pages.pim import PimPage

@pytest.mark.usefixtures("setup_and_teardown")
class Test_TC000_Login:
    def test_login_logout(self):
        with allure.step("Login to the application"):
            login_page = LoginPage(self.driver)
            assert login_page.verify_the_login_page()
            credentials = Excel_Utils.fetch_data_as_dicts("Credentials")
            dashboard_page = login_page.login_to_the_application(credentials["Username"], credentials["Password"])
            assert dashboard_page.verify_the_dashboard_page()

        with allure.step("Log out from the application"):
            login_page.logout_from_the_application()
            assert login_page.verify_the_login_page()
