from requests import get, post, delete

# print(get('http://127.0.0.1:8080/api/users').json())
# print(post('http://127.0.0.1:8080/api/users', json={'login': 'alex3',
#                                                     'name': 'jt',
#                                                     'password': '123',
#                                                     'email': '12433@yandex.ru',
#                                                     'photo': 'ale'}).json())
print(get('http://127.0.0.1:8080/api/users').json())
