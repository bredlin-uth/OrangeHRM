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
class Test_TC003_Leave:
    def test_apply_leave(self):

        with allure.step("Login to the application"):
            login_page = LoginPage(self.driver)
            assert login_page.verify_the_login_page()
            credentials = Excel_Utils.fetch_data_as_dicts("Credentials")
            dashboard_page = login_page.login_to_the_application(credentials["Username"], credentials["Password"])
            assert dashboard_page.verify_the_dashboard_page()

        with allure.step("Apply Leave"):
            dashboard_page.click_on_menu_item("Leave")
            leave_page = LeavePage(self.driver)
            assert leave_page.verify_the_leave_page()
            leave_page.click_on_apply_tab()
            apply_leave = Excel_Utils.fetch_data_as_dicts("Leave")
            leave_page.apply_leave(apply_leave["leave_type"], apply_leave["from_date"], apply_leave["to_date"], apply_leave["comments"])
            assert leave_page.verify_the_success_toast()
            leave_page.click_on_my_leave_tab()
            assert leave_page.verify_the_applied_leave(apply_leave["leave_type"], apply_leave["comments"])

        with allure.step("Log out from the application"):
            login_page.logout_from_the_application()
            assert login_page.verify_the_login_page()