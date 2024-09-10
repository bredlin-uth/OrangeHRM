import allure
import pytest

from generic_utils import Excel_Utils, Config_Utils
from pages.leave import LeavePage
from pages.login_logout import LoginPage

@pytest.mark.usefixtures("setup_and_teardown", "screenshot_on_failure")
class Test_TC003_Leave:
    def test_apply_leave(self):
        excel_path = Config_Utils.get_config("directory info", "excel_path")
        with allure.step("Login to the application"):
            login_page = LoginPage(self.driver)
            assert login_page.verify_the_login_page()
            credentials = Excel_Utils.fetch_data_as_dicts("Credentials")
            Excel_Utils.write_data_to_excel(excel_path, "Apply Leave", credentials)
            dashboard_page = login_page.login_to_the_application(credentials["Username"], credentials["Password"])
            assert dashboard_page.verify_the_dashboard_page()

        with allure.step("Apply Leave"):
            dashboard_page.click_on_menu_item("Leave")
            leave_page = LeavePage(self.driver)
            assert leave_page.verify_the_leave_page()
            leave_page.click_on_apply_tab()
            apply_leave = Excel_Utils.fetch_data_as_dicts("Leave")
            Excel_Utils.write_data_to_excel(excel_path, "Apply Leave", apply_leave)
            leave_page.apply_leave(apply_leave["leave_type"], apply_leave["from_date"], apply_leave["to_date"], apply_leave["comments"])
            success_message = leave_page.verify_the_success_toast()
            Excel_Utils.write_data_to_excel(excel_path, "Apply Leave", success_message)
            leave_page.click_on_my_leave_tab()
            assert leave_page.verify_the_applied_leave(apply_leave["leave_type"], apply_leave["comments"])

        with allure.step("Log out from the application"):
            login_page.logout_from_the_application()
            assert login_page.verify_the_login_page()