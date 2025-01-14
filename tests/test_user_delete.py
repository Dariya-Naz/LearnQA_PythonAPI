import requests
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import time

class TestUserDelete(BaseCase):
    def test_user2_delete(self):
        # LOGIN
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")


        Assertions.assert_code_status(response1, 200)
        Assertions.assert_response_text(response1, '{"user_id":2}')

        # DELETE
        response2 = MyRequests.delete(f"/user/2",
                                headers={"x-csrf-token": token},
                                cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_response_text(response2, '{"error":"Please, do not delete test users with ID 1, 2, 3, 4 or 5."}')

    def test_user_delete_success(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        firstName = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id = self.get_json_value(response2, "user_id")

        Assertions.assert_code_status(response2, 200)

        # DELETE
        response3 = MyRequests.delete(f"/user/{user_id}",
                                headers={"x-csrf-token": token},
                                cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_response_text(response3, '{"success":"!"}')

        # Check, that user was successfully deleted
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response4, 404)
        Assertions.assert_response_text(response4, 'User not found')

    def test_try_to_delete_another_user(self):
        # REGISTER user#1
        register_data1 = self.prepare_registration_data()
        response1 = requests.post('https://playground.learnqa.ru/api/user', data=register_data1)
        user_id1 = self.get_json_value(response1, "id")

        # REGISTER user#2
        time.sleep(2)
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post(f"/user", data=register_data2)

        # LOGIN user#2
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

        response4 = MyRequests.delete(f"/user/{user_id1}",
                                      cookies={"auth_sid": auth_sid2},
                                      headers={"x-csrf-token": token2})
        Assertions.assert_code_status(response4, 400)
        Assertions.assert_response_text(response4, '{"error":"This user can only delete their own account."}')
