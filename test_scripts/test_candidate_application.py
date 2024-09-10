import allure
import pytest

from generic_utils import Excel_Utils, Config_Utils
from pages.login_logout import LoginPage
from pages.recruitment import RecruitmentPage

@pytest.mark.usefixtures("setup_and_teardown", "screenshot_on_failure")
class Test_TC004_Recruitment:
    def test_candidate_application(self):
        excel_path = Config_Utils.get_config("directory info", "excel_path")
        with allure.step("Login to the application"):
            login_page = LoginPage(self.driver)
            assert login_page.verify_the_login_page()
            credentials = Excel_Utils.fetch_data_as_dicts("Credentials")
            Excel_Utils.write_data_to_excel(excel_path, "Candidate Application", credentials)
            dashboard_page = login_page.login_to_the_application(credentials["Username"], credentials["Password"])
            assert dashboard_page.verify_the_dashboard_page()

        with allure.step("Candidate Application"):
            dashboard_page.click_on_menu_item("Recruitment")
            recruitment_page = RecruitmentPage(self.driver)
            assert recruitment_page.verify_the_recruitment_page()
            recruitment_page.click_on_add_button()
            recruitment = Excel_Utils.fetch_data_as_dicts("Recruitment")
            Excel_Utils.write_data_to_excel(excel_path, "Candidate Application", recruitment)
            recruitment_page.add_candidate(recruitment["name"], recruitment["vacancy"], recruitment["email"], recruitment["contact"],
                                           recruitment["data"], recruitment["notes"], recruitment["file_path"])
            success_message = recruitment_page.verify_the_success_toast()
            Excel_Utils.write_data_to_excel(excel_path, "Candidate Application", success_message)
            assert recruitment_page.verify_the_candidate_application(recruitment["name"], recruitment["vacancy"])

        with allure.step("Log out from the application"):
            login_page.logout_from_the_application()
            assert login_page.verify_the_login_page()