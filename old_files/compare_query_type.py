import requests
print ("1 point:")
a=requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(a.text)
print(a.status_code)

print ("2 point:")
a=requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": "HEAD"})
print("Status code is ", a.status_code)


print ("4 point (contains 3 point):")
for method in ["get", "post", "put", "delete"]:
    for data in [{"method": "GET"}, {"method": "POST"}, {"method": "PUT"}, {"method": "DELETE"}]:
        if method == "get":
            response = requests.request(method=method, url="https://playground.learnqa.ru/ajax/api/compare_query_type", params=data)
        else:
            response = requests.request(method=method, url="https://playground.learnqa.ru/ajax/api/compare_query_type", data=data)
        print("Result for method ", method, "whith parameter ", data, ":", response.text)