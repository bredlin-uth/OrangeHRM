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
class Test_Runner:
    def test_orange_hrm(self):

        with allure.step("Login to the application"):
            login_page = LoginPage(self.driver)
            assert login_page.verify_the_login_page()
            credentials = Excel_Utils.fetch_data_as_dicts("Credentials")
            dashboard_page = login_page.login_to_the_application(credentials["Username"], credentials["Password"])
            assert dashboard_page.verify_the_dashboard_page()

        with allure.step("Add User"):
            dashboard_page.click_on_menu_item("Admin")
            admin_page = AdminPage(self.driver)
            assert admin_page.verify_the_admin_page()
            admin_page.select_users_from_the_dropdown("User Management", "Users")
            admin_page.click_on_add_button()
            add_user = Excel_Utils.fetch_data_as_dicts("Add User")
            username = admin_page.add_user(add_user["user_role"], add_user["status"], add_user["employee_name"], add_user["username"], add_user["password"])
            assert admin_page.verify_the_success_toast()
            assert admin_page.verify_the_user_in_the_record(username)

        with allure.step("Delete User"):
            username = admin_page.delete_user(username)
            assert admin_page.verify_the_user_is_deleted(username)

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

        with allure.step("Candidate Application"):
            dashboard_page.click_on_menu_item("Recruitment")
            recruitment_page = RecruitmentPage(self.driver)
            assert recruitment_page.verify_the_recruitment_page()
            recruitment_page.click_on_add_button()
            recruitment = Excel_Utils.fetch_data_as_dicts("Recruitment")
            recruitment_page.add_candidate(recruitment["name"], recruitment["vacancy"], recruitment["email"], recruitment["contact"],
                                           recruitment["data"], recruitment["notes"], recruitment["file_path"])
            assert recruitment_page.verify_the_success_toast()
            assert recruitment_page.verify_the_candidate_application(recruitment["name"], recruitment["vacancy"])

        with allure.step("Candidate Resume Download"):
            dashboard_page.click_on_menu_item("Recruitment")
            recent_file = recruitment_page.download_candidate_resume()
            print("Recently Downloaded file:", recent_file)

        with allure.step("Add/Update Personal Details"):
            dashboard_page.click_on_menu_item("My Info")
            my_info_page = MyInfoPage(self.driver)
            assert my_info_page.verify_the_info_page()
            personal = Excel_Utils.fetch_data_as_dicts("My Info")
            my_info_page.add_personal_details(personal["name"], personal["employee_id"], personal["other_id"], personal["licence_number"], personal["expiry_date"],
                                              personal["nationality"], personal["marital_status"], personal["date_of_birth"], personal["gender"])
            assert my_info_page.verify_the_success_toast()

        with allure.step("Download and Verify Personal Details"):
            assert my_info_page.verify_the_profile_record()

        with allure.step("Orange HRM Help"):
            dashboard_page.click_on_menu_item("PIM")
            pim_page = PimPage(self.driver)
            assert pim_page.verify_the_pim_page()
            pim_page.verify_orange_hrm_help(Config_Utils.get_config("url info", "help_url"))

        with allure.step("Extract Data from Canvas"):
            dashboard_page.click_on_menu_item("Dashboard")
            text = dashboard_page.extract_data_from_canvas()
            last_row = Excel_Utils.get_row_count("Pie Chart")
            Excel_Utils.write_data_into_excel("Pie Chart", last_row + 1, 1, text)

        with allure.step("Log out from the application"):
            login_page.logout_from_the_application()
            assert login_page.verify_the_login_page()
