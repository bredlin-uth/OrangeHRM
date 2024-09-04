import allure
import pytest

from generic_utils import Excel_Utils, Config_Utils
from pages.admin import AdminPage
from pages.leave import LeavePage
from pages.login_logout import LoginPage
from pages.my_info import MyInfoPage
from pages.pim import PimPage
from pages.recruitment import RecruitmentPage

@pytest.mark.usefixtures("setup_and_teardown")
class Test_TC009_PIM:
    def test_switch_between_tabs(self):

        with allure.step("Login to the application"):
            login_page = LoginPage(self.driver)
            assert login_page.verify_the_login_page()
            credentials = Excel_Utils.fetch_data_as_dicts("Credentials")
            dashboard_page = login_page.login_to_the_application(credentials["Username"], credentials["Password"])
            assert dashboard_page.verify_the_dashboard_page()

        with allure.step("Orange HRM Help"):
            dashboard_page.click_on_menu_item("PIM")
            pim_page = PimPage(self.driver)
            assert pim_page.verify_the_pim_page()
            pim_page.verify_orange_hrm_help(Config_Utils.get_config("url info", "help_url"))

        with allure.step("Log out from the application"):
            login_page.logout_from_the_application()
            assert login_page.verify_the_login_page()
