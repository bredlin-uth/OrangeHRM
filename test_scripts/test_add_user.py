import allure
import pytest

from generic_utils import Excel_Utils, Config_Utils
from pages.admin import AdminPage
from pages.login_logout import LoginPage

@pytest.mark.usefixtures("setup_and_teardown", "screenshot_on_failure")
class Test_TC001_Admin:
    def test_add_user(self):
        excel_path = Config_Utils.get_config("directory info", "excel_path")
        with allure.step("Login to the application"):
            login_page = LoginPage(self.driver)
            assert login_page.verify_the_login_page()
            credentials = Excel_Utils.fetch_data_as_dicts("Credentials")
            Excel_Utils.write_data_to_excel(excel_path, "Add User", credentials)
            dashboard_page = login_page.login_to_the_application(credentials["Username"], credentials["Password"])
            assert dashboard_page.verify_the_dashboard_page()

        with allure.step("Add User"):
            dashboard_page.click_on_menu_item("Admin")
            admin_page = AdminPage(self.driver)
            assert admin_page.verify_the_admin_page()
            admin_page.select_users_from_the_dropdown("User Management", "Users")
            admin_page.click_on_add_button()
            add_user = Excel_Utils.fetch_data_as_dicts("Add User")
            Excel_Utils.write_data_to_excel(excel_path, "Add User", add_user)
            username = admin_page.add_user(add_user["user_role"], add_user["status"], add_user["employee_name"], add_user["username"], add_user["password"])
            success_message = admin_page.verify_the_success_toast()
            Excel_Utils.write_data_to_excel(excel_path, "Add User", success_message)
            assert admin_page.verify_the_user_in_the_record(username)

        with allure.step("Log out from the application"):
            login_page.logout_from_the_application()
            assert login_page.verify_the_login_page()