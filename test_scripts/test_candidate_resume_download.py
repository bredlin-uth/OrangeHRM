import allure
import pytest

from generic_utils import Excel_Utils, Config_Utils
from pages.login_logout import LoginPage
from pages.recruitment import RecruitmentPage

@pytest.mark.usefixtures("setup_and_teardown", "screenshot_on_failure")
class Test_TC005_Recruitment:
    def test_candidate_resume_download(self):
        excel_path = Config_Utils.get_config("directory info", "excel_path")
        with allure.step("Login to the application"):
            login_page = LoginPage(self.driver)
            assert login_page.verify_the_login_page()
            credentials = Excel_Utils.fetch_data_as_dicts("Credentials")
            Excel_Utils.write_data_to_excel(excel_path, "Resume Download", credentials)
            dashboard_page = login_page.login_to_the_application(credentials["Username"], credentials["Password"])
            assert dashboard_page.verify_the_dashboard_page()

        with allure.step("Candidate Resume Download"):
            dashboard_page.click_on_menu_item("Recruitment")
            recruitment_page = RecruitmentPage(self.driver)
            recent_file = recruitment_page.download_candidate_resume()
            Excel_Utils.write_data_to_excel(excel_path, "Resume Download", {"Recently Downloaded file": recent_file})

        with allure.step("Log out from the application"):
            login_page.logout_from_the_application()
            assert login_page.verify_the_login_page()