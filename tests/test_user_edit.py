import allure
import requests
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import time

@allure.epic("Tests for user edit")
class TestUserEdit(BaseCase):
    @allure.description("Create and edit user")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_edit_just_created_user(self):
        with allure.step("Register user"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response1,200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            firstName = register_data['firstName']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        with allure.step("Login user"):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        with allure.step("EDIT"):
            new_name = "Changed Name"

            response3 = MyRequests.put(f"/user/{user_id}",
                                    headers={"x-csrf-token":token},
                                    cookies={"auth_sid":auth_sid},
                                    data={"firstName":new_name})

            Assertions.assert_code_status(response3, 200)

        with allure.step("GET"):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
                )

            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                new_name,
                "Wrong name of the user after edit"
            )

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This case checks editing not authorized user")
    def test_edit_not_authorized_user(self):
        with allure.step("REGISTER"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response1,200)
            Assertions.assert_json_has_key(response1, "id")

            user_id = self.get_json_value(response1, "id")

        with allure.step("EDIT"):
            new_name = "Changed Name"

            response3 = MyRequests.put(f"/user/{user_id}",
                                    data={"firstName": new_name})

            Assertions.assert_code_status(response3, 400)
            Assertions.assert_response_text(response3, '{"error":"Auth token not supplied"}')

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This case checks, that user cannot edit another one")
    def test_try_to_edit_another_user(self):
        with allure.step("REGISTER user#1"):
            register_data1 = self.prepare_registration_data()
            response1 = requests.post('https://playground.learnqa.ru/api/user', data=register_data1)
            user_id1 = self.get_json_value(response1, "id")

        with allure.step("REGISTER user#2"):
            time.sleep(2)
            register_data2 = self.prepare_registration_data()
            response2 = MyRequests.post(f"/user", data=register_data2)

        with allure.step("LOGIN user#2"):
            email2 = register_data2['email']
            password2 = register_data2['password']

            data = {
                'email': email2,
                'password': password2
            }
            response3 = MyRequests.post('/user/login', data=data)

            auth_sid2 = BaseCase.get_cookie(self, response3, "auth_sid")
            token2 = BaseCase.get_header(self, response3, headers_name="x-csrf-token")

            cookies = response3.cookies["auth_sid"]
            token2 = response3.headers["x-csrf-token"]

        with allure.step("TRY to edit user#1 by user#2"):
            new_name = "Changed name"
            response4 = MyRequests.put(f"/user/{user_id1}",
                                    cookies={"auth_sid": auth_sid2},
                                    headers={"x-csrf-token": token2},
                                    data={"firstName": new_name})

            Assertions.assert_code_status(response4, 400)
            Assertions.assert_response_text(response4, '{"error":"This user can only edit their own data."}')

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("This case checks, that registration without '@' is impossinble")
    def test_change_user_email_without_at(self):
        with allure.step("REGISTER"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            firstName = register_data['firstName']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        with allure.step("LOGIN"):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        with allure.step("EDIT"):

            email = email.replace('@', '')

            response3 = MyRequests.put(f"/user/{user_id}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid},
                                    data={"email": email})

            Assertions.assert_code_status(response3, 400)
            Assertions.assert_response_text(response3, '{"error":"Invalid email format"}')

    @allure.severity(allure.severity_level.MINOR)
    @allure.description("This case checks, that firstname with one letter is too short")
    def test_change_user_firstname_with_one_letter(self):
        with allure.step("REGISTER"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            firstName = register_data['firstName']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        with allure.step("LOGIN"):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        with allure.step("EDIT"):
            firstName = 'a'

            response3 = MyRequests.put(f"/user/{user_id}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid},
                                    data={"firstName": firstName})

            Assertions.assert_code_status(response3, 400)
            Assertions.assert_response_text(response3, '{"error":"The value for field `firstName` is too short"}')