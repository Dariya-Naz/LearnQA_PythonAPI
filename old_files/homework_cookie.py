import requests

class TestCookie:

    def test_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookie_value = response.cookies.get('HomeWork')
        print("Cookie is: ", cookie_value)

        assert cookie_value == 'hw_value', "Cookie value does not match with expected cookie"