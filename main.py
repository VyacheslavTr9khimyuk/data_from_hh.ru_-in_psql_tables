from src.function_get_hh_ru import get_hh_ru_data
from src.function_get_data_dict import get_data_for_database
from src.function_create import create_database
from src.function_save import save_data_to_database
from src.DBManager import DBManager

from config import config


def main():
    # текст поискового запроса по вакансиям на сайте hh.ru
    text_filter = 'Developer'

    # название базы данных для сохранения данных о вакансиях
    db_name = 'db_vacancies'

    params = config()

    # собираем вакансии
    get_hh_ru_data(text_filter)

    # обрабатываем данные о вакансиях для сохранения в базу данных
    data_dict = get_data_for_database()

    # создаем базу данных в PostgreSQL
    create_database(db_name, params)

    # сохраняем данные о вакансиях и компаниях-работодателях в базу данных
    save_data_to_database(data_dict, db_name, params)

    # создаем экземпляр класса DBManager для созданной базы данных
    dbm = DBManager(db_name, params)

    # вызовем фуекцию для вывода списка всех компаний и количество вакансий у каждой компании
    dbm.get_companies_and_vacancies_count()

    # вызовем фуекцию для вывода списка всех вакансий с указанием названия компании, названия
    # вакансии и зарплаты и ссылки на вакансию
    dbm.get_all_vacancies()

    # вызовем фуекцию для вывода средней зарплаты по вакансиям
    dbm.get_avg_salary()

    # вызовем фуекцию для вывода список всех вакансий, у которых зарплата выше средней по всем вакансиям
    dbm.get_vacancies_with_higher_salary()

    # попросим пользователя ввести интересующее в вакансии слово
    word = input("Введите ключевое слово в названии вакансии (например, python): ")
    # вызовем фуекцию для вывода список всех вакансий, в названии которых содержится
    # переданное в метод слово
    dbm.get_vacancies_with_keyword(word)


if __name__ == '__main__':
    main()