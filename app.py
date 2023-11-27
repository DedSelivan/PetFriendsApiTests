import requests
import json
from requests_toolbelt import MultipartEncoder

import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """API-библиотека к веб приложению PetFriends"""

    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API-сервера и возвращает статус запроса и результат в формате JSON с уникальным
        ключём пользователя """
        headers = {
            'email': email,
            'password': password
        }
        response = requests.get(self.base_url + '/api/key', headers=headers)
        status_code = response.status_code
        result = ''
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text
        return status_code, result

    def get_list_of_pets(self, auth_key: json, filter: str = '') -> json:
        """Метод делает запрос API-сервера и возвращает статус запроса и результат в формате JSON со списком всех
        найденых питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
        либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
        собственных питомцев"""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        response = requests.get(self.base_url + '/api/pets', headers=headers, params=filter)
        status_code = response.status_code
        result = ''
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text
        return status_code, result

    def add_information_about_new_pet(self, auth_key: json, name: str, animal_type: str, age: int, pet_photo: str) \
            -> json:
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': ('bull.jpeg', open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        response = requests.post(self.base_url + '/api/pets', headers=headers, data=data)
        status = response.status_code
        result = ""
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text
        return status, result

    def add_information_about_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) \
            -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
           запроса на сервер и результат в формате JSON с данными добавленного питомца"""
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        headers = {'auth_key': auth_key['key']}
        response = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status_code = response.status_code
        result = ""
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text
        return status_code, result

    def add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет (постит) на сервер данные с изображением питомца и возвращает статус запроса и
        result в формате JSON с обновлённым изображением питомца"""
        data = MultipartEncoder(
            fields={
                'pet_photo': ('dog.jpg', open(pet_photo, 'rb'), 'image/jpeg')
            }
        )
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        response = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status_code = response.status_code
        result = ""
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text
        return status_code, result

    def delete_pet_from_database(self, auth_key: json, pet_id: str):
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
           статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
           На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""
        headers = {'auth_key': auth_key['key']}

        response = requests.delete(self.base_url + '/api/pets/' + pet_id, headers=headers)
        status = response.status_code
        result = ""
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text
        return status, result

    def update_information_about_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int):
        """Метод отправляет запрос на сервер о обновлении данных питомуа по указанному ID и
           возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        response = requests.put(self.base_url + '/api/pets/' + pet_id, headers=headers, data=data)
        status_code = response.status_code
        result = ''
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text
        return status_code, result

    def add_new_pet_simple(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
           запроса и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        response = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = response.status_code
        result = ''
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text
        print(result)
        return status, result