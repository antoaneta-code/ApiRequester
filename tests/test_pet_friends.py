import json

import pytest
import os
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

def test_get_api_key_for_invalid_user():
    """Проверяем, что возникает ошибка при полючении токена с неверными логином и паролем"""
    status, result = pf.get_api_key('bad_email', 'bad_password')
    assert status == 403

def test_get_api_key_for_valid_user():
    """Проверяем успешное получение токена с валидными логином и паролем"""
    status, result = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in result

def test_success_get_all_pets():
    """Проверка успешности метода получения списка всех животных"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, '')
    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_invalid_user():
    """Проверка отказа метода с невалидным токеном"""
    _, auth_key = pf.get_api_key('any_email', 'any_password')
    status, result = pf.get_list_of_pets(auth_key, '')
    assert status == 403

def test_add_new_pet_with_valid_info():
    """Проверяем что можно добавить питомца с корректными данными"""
    name = 'Собакевич'
    animal_type = 'корги'
    age = 2

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == str(age)

def test_add_new_pet_with_invalid_age():
   """Проверяем, что можно добавить питомца с корректными данными"""
   name = 'Васька'
   animal_type = 'дворняга'
   age = 'три'

   # Запрашиваем ключ api и сохраняем в переменую auth_key
   _, auth_key = pf.get_api_key(valid_email, valid_password)

   # Добавляем питомца
   status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

   # Сверяем полученный ответ с ожидаемым результатом
   assert status == 400


def test_successful_update_pet_age():
    """Проверка успешного обновления данных питомца"""
    name = 'Пушок'
    animal_type = 'Кот'
    age = 8
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    pet_id = result['id']
    new_age = 5
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, new_age)
    assert status == 200
    assert result['age'] == str(new_age)

def test_successful_update_pet_name():
    """Проверка успешного обновления имени питомца"""
    name = 'Сашок'
    animal_type = 'Бегемот'
    age = 13
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    pet_id = result['id']

    new_name = 'Горшок'
    status, result = pf.update_pet_info(auth_key, pet_id, new_name, animal_type, age)
    assert status == 200
    assert result['name'] == new_name

def test_successful_delete_self_pet():
    """Проверка успешного удаления питомца"""
    name = 'Хома'
    animal_type = 'хомяк'
    age = 13
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    pet_id = result['id']

    status, result = pf.delete_pet(auth_key, pet_id)
    assert status == 200

    status, all_pets = pf.get_list_of_pets(auth_key, '')

    del_res = [pet for pet in all_pets['pets'] if pet['id'] == pet_id]

    assert del_res == []

def test_unsuccesful_try_delete_twice_pet():
    """Проверка неуспешного повторного удаления питомца"""
    name = 'Кузя'
    animal_type = 'енот'
    age = 13
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    pet_id = result['id']

    status, result = pf.delete_pet(auth_key, pet_id)
    status, result = pf.delete_pet(auth_key, pet_id)

    assert status == 200