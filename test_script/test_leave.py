import time

import pytest

from generic_utils import Config_Utils
from pages.admin import AdminPage
from pages.leave import LeavePage
from pages.login_logout import LoginPage

@pytest.mark.usefixtures("setup_and_teardown")
class Test_T003_Leave:
    def test_delete_user(self):
        login_page = LoginPage(self.driver)
        assert login_page.verify_the_login_page()
        username = Config_Utils.get_config("credential info", "username")
        password = Config_Utils.get_config("credential info", "password")
        dashboard_page = login_page.login_to_the_application(username, password)
        assert dashboard_page.verify_the_dashboard_page()

        dashboard_page.click_on_menu_item("Leave")
        leave_page = LeavePage(self.driver)
        assert leave_page.verify_the_leave_page()
        leave_page.click_on_apply_tab()
        leave_page.apply_leave("CAN - FMLA", "4 September 2024", "5 September 2024", "not feeling good")
        assert leave_page.verify_the_success_toast()
        assert leave_page.verify_the_applied_leave("CAN - FMLA", "not feeling good")

        login_page.logout_from_the_application()
        assert login_page.verify_the_login_page()
