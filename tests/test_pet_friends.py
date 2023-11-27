from app import PetFriends
from setting import valid_email, valid_password
import os

pet_friends = PetFriends()


def test_get_api_key(email=valid_email, password=valid_password):
    """Проверяем что запрос API-ключа возвращает статус 200 и в результате содержится 'key'"""

    # Отправляем запрос и сохраняем полученный ответ со статусом кода в переменную status_code,
    # а текст ответа в переменную result
    status_code, result = pet_friends.get_api_key(email, password)
    # Сверяем полученный результат с ожидаемым
    assert status_code == 200
    assert 'key' in result


def test_add_information_about_new_pet(name='Ragnar', animal_type='Бык', age='4', pet_photo='images/bull.jpeg'):
    """Проверяем возможность добавления нового питомца"""

    # Получаем путь изображения питомца и сохраняем его в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем API-ключ и сохраняем в переменную auth_key
    _, auth_key = pet_friends.get_api_key(valid_email, valid_password)
    # Добавляем нашего питомца
    status_code, result = pet_friends.add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный результат с ожидаемым
    assert status_code == 200
    assert result['name'] == name


def test_add_information_about_new_pet_without_photo(name='Рагнар', animal_type='Бык', age='4'):
    """Проверяем возможность добавления питомца без фото"""
    # Получаем API-ключ и сохраняем в переменную auth_key
    _, auth_key = pet_friends.get_api_key(valid_email, valid_password)
    # Добавляем нашего питомца
    status_code, result = pet_friends.add_information_about_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный результат с ожидаемым
    assert status_code == 200
    assert result['name'] == name


def test_add_photo_of_pet(pet_photo='images/dog.jpg'):
    """Проверяем возможность добавить изображение питомцу без фото"""

    # Получаем путь изображения питомца и сохраняем его в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем API-ключ и сохраняем в переменную auth_key
    _, auth_key = pet_friends.get_api_key(valid_email, valid_password)
    # Запрашиваем список питомцев
    _, my_pets = pet_friends.get_list_of_pets(auth_key, 'my_pets')
    # Присваиваем переменной pet_id, значение id питомца
    pet_id = my_pets['pets'][0]['id']
    # Добавляем изображение нашему питомцу
    status_code, result = pet_friends.add_photo_of_pet(auth_key, pet_id, pet_photo)
    # Сверяем полученный результат с ожидаемым
    assert status_code == 200
    assert result['pet_photo'] != ''


def test_get_list_of_pets(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Доступное значение параметра filter - 'my_pets' либо '' """

    # Для этого сначала получаем API-ключ и сохраняем в переменную auth_key.
    # Далее используя этого ключ запрашиваем список всех питомцев.
    _, auth_key = pet_friends.get_api_key(valid_email, valid_password)
    status_code, result = pet_friends.get_list_of_pets(auth_key, filter)
    # Сверяем полученный результат с ожидаемым
    assert status_code == 200
    assert len(result['pets']) > 0


def test_update_information_about_pet(name='Гриша', animal_type='Лось', age='8'):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем auth_key и список своих питомцев
    _, auth_key = pet_friends.get_api_key(valid_email, valid_password)
    _, my_pets = pet_friends.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status_code, result = pet_friends.update_information_about_pet(auth_key, my_pets['pets'][0]['id'], name,
                                                                       animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status_code == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == age
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_delete_pet_from_database():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pet_friends.get_api_key(valid_email, valid_password)
    _, my_pets = pet_friends.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем - если список пустой, то добавляем нового пользователя и опять запрашиваем список питомцев
    if len(my_pets['pets']) == 0:
        pet_friends.add_information_about_new_pet_without_photo(auth_key, 'Петя', 'Пума', '18')
        _, my_pets = pet_friends.get_list_of_pets(auth_key, 'my_pets')

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][1]['id']
    status_code, _ = pet_friends.delete_pet_from_database(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pet_friends.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем что статус ответа равен 200 и в списке питомцев , нету питомца с удалённым id
    assert status_code == 200
    assert pet_id is not my_pets.values()