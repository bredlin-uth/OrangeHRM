import allure
import pytest

from generic_utils import Excel_Utils, Config_Utils
from pages.login_logout import LoginPage
from pages.pim import PimPage

@pytest.mark.usefixtures("setup_and_teardown", "screenshot_on_failure")
class Test_TC009_PIM:
    def test_switch_between_tabs(self):
        excel_path = Config_Utils.get_config("directory info", "excel_path")
        with allure.step("Login to the application"):
            login_page = LoginPage(self.driver)
            assert login_page.verify_the_login_page()
            credentials = Excel_Utils.fetch_data_as_dicts("Credentials")
            Excel_Utils.write_data_to_excel(excel_path, "Help", credentials)
            dashboard_page = login_page.login_to_the_application(credentials["Username"], credentials["Password"])
            assert dashboard_page.verify_the_dashboard_page()

        with allure.step("Orange HRM Help"):
            dashboard_page.click_on_menu_item("PIM")
            pim_page = PimPage(self.driver)
            assert pim_page.verify_the_pim_page()
            pim_page.verify_orange_hrm_help(Config_Utils.get_config("url info", "help_url"))
            Excel_Utils.write_data_to_excel(excel_path, "Help", "Able to switch between Tabs")

        with allure.step("Log out from the application"):
            login_page.logout_from_the_application()
            assert login_page.verify_the_login_page()
