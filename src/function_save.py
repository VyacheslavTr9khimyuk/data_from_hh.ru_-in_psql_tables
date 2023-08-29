import psycopg2
from typing import Any


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранение данных о вакансиях и компаниях-работодателях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for dt in data:
            cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, vacancy_name, experience, description, 
                salary_from, salary_to, salary_currency, company_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (dt['vacancy_id'], dt['vacancy_name'], dt['experience'], dt['description'],
                 dt['salary_from'], dt['salary_to'], dt['salary_currency'], dt['company_id'])
            )
            cur.execute(
                """
                INSERT INTO companies (company_id, company_name)
                VALUES (%s, %s)
                """,
                (dt['company_id'], dt['company_name'])
            )

    conn.commit()
    conn.close()

    print("Данные о вакансиях и компаниях-работодателях сохранены в базу данных")
