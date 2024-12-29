import requests

class TestHeader:

    def test_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        print (response.headers)
        header_value = response.headers.get('x-secret-homework-header')
        print("Header value is: ", header_value)

        assert header_value == 'Some secret value', "Header value does not match with expected header"