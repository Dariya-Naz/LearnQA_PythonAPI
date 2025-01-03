import requests


#
# response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data = payload, params = payload)
# print(response.text)


response = requests.request(method='connect', url="https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": "CONNECT"})
print (response.text)

