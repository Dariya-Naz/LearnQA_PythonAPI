import requests
import json
import time

#Запрос на создание задачи
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")

#Парсинг JSON-а
obj = json.loads(response.text)
to_ken = obj['token']
seconds = obj['seconds']
if response.status_code == 200 and 'token' in obj:
    print("Задача создана успешно, ждите.\n")
else:
    print('Задача не создалась')

#Первый запрос на проверку выполнения задачи
time.sleep(seconds-5)
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params = {'token': to_ken})
print(response.text)

#Проверка поля "status"
obj_1 = json.loads(response.text)
if obj_1["status"] == "Job is NOT ready":
    print ("Задача еще не готова, поле status корректно.\n")
else: print("fail")

#Второй запрос на проверку выполнения задачи
time.sleep(5)
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params = {'token': to_ken})
print(response.text)

#Проверка поля "status" и наличия поля "result"
obj_2 = json.loads(response.text)
if obj_2["status"] == "Job is ready":
    print ("Задача готова. Поле status корректно.")
else: print("fail")

if 'result' in obj_2:
    print("Поле result присутсвует.")
else:
    print ('Поле result отсутсвует')