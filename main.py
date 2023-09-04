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

    print(f"БД {db_name} успешно создана")



if __name__ == '__main__':
    main()