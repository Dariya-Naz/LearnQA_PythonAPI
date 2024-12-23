import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
list = (response.history)
amount = len (list)
print ("Количество редиректов:", amount)
print ("Конечный url:", response.url)