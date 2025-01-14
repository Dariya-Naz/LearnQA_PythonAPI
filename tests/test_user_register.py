import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


class TestUserRegister(BaseCase):
    element_for_delete = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()


        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data = data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content '{response.content}'"

    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_without_at(self):
        email = 'dariyaexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data = data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, "Invalid email format")

    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.parametrize('element_for_delete', element_for_delete)
    def test_create_user_with_one_missed_parameter(self, element_for_delete):
        data = self.prepare_registration_data()
        del data[element_for_delete]

        response = MyRequests.post("/user", data = data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, f"The following required params are missed: {element_for_delete}")

    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_with_too_short_username(self):
        data = self.prepare_registration_data(self, username='a')

        response = MyRequests.post("/user", data = data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, 'The value of \'username\' field is too short')

    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_with_too_long_username(self):
        long_user_name = 'hfudhfsjdfljsdlksdjcldsjsjedpijedjeojdpoejdpjepdojddfjvglkdfjlksdjflsjdfcoihsdicugbsdbcisdnlicksdlkcnlskdnclsndclknsdlkcfnslkdnclksdnclklksdnlckndpoejdpjepdojddfjvglkdfjlksdjflsjdfcoihsdicugbsdbcisdnlicksdlkcnlkdnclsndclknsdlkcnslkdnclksdnclksdsdnlckn'
        data = self.prepare_registration_data(self, username=long_user_name)

        response = MyRequests.post("/user", data = data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, 'The value of \'username\' field is too long')