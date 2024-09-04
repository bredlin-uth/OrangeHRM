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
class Test_TC007_MyInfo:
    def test_download_personal_details(self):

        with allure.step("Login to the application"):
            login_page = LoginPage(self.driver)
            assert login_page.verify_the_login_page()
            credentials = Excel_Utils.fetch_data_as_dicts("Credentials")
            dashboard_page = login_page.login_to_the_application(credentials["Username"], credentials["Password"])
            assert dashboard_page.verify_the_dashboard_page()

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

        with allure.step("Log out from the application"):
            login_page.logout_from_the_application()
            assert login_page.verify_the_login_page()
