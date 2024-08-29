import pytest

from generic_utils import Config_Utils
from pages.admin import AdminPage
from pages.login_logout import LoginPage

@pytest.mark.usefixtures("setup_and_teardown")
class Test_T002_Admin:
    def test_delete_user(self):
        login_page = LoginPage(self.driver)
        assert login_page.verify_the_login_page()
        username = Config_Utils.get_config("credential info", "username")
        password = Config_Utils.get_config("credential info", "password")
        dashboard_page = login_page.login_to_the_application(username, password)
        assert dashboard_page.verify_the_dashboard_page()

        dashboard_page.click_on_menu_item("Admin")
        admin_page = AdminPage(self.driver)
        assert admin_page.verify_the_admin_page()
        admin_page.select_users_from_the_dropdown("User Management", "Users")

        username = admin_page.delete_user()
        assert admin_page.verify_the_user_is_deleted(username)
