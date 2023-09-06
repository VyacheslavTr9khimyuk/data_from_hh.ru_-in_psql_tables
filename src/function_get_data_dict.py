import json
import os
from typing import Any


def get_data_for_database() -> list[dict[str, Any]]:
    """
    Функция получения списка данных из файлов для сохранения в базу данных
    Вовзращает список множеств data_dict
    """
    # Создание списка для столбцов таблицы vacancy
    data_dict = []

    # Перебор всех файлов в папке vacancies
    for fl in os.listdir('./src/docs/vacancies'):
        # Открытие, чтение, закрытие файла
        f = open(f'./src/docs/vacancies/{fl}', encoding='utf8')
        json_text = f.read()
        f.close()
        # Перевод текста файла в словарь
        json_dict = json.loads(json_text)

        # Условие для проверки, указана зарплата или нет
        if json_dict['salary'] is not None:
            s_from = json_dict['salary']['from']
            s_to = json_dict['salary']['to']
            s_currency = json_dict['salary']['currency']
        else:
            s_from = None
            s_to = None
            s_currency = None

        # Добавление в список множества с данными по вакансии
        data_dict.append({
            'vacancy_id' : json_dict['id'],
            'vacancy_name' : json_dict['name'],
            'vacancy_url' : json_dict['alternate_url'],
            'area_id' : json_dict['area']['id'],
            'area_name' : json_dict['area']['name'],
            'experience' : json_dict['experience']['name'],
            'description' : json_dict['description'],
            'salary_from' : s_from,
            'salary_to' : s_to,
            'salary_currency' : s_currency,
            'company_id' : json_dict['employer']['id'],
            'company_name' : json_dict['employer']['name']
        })

    print('Файлы обработаны')

    return data_dict
