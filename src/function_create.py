import psycopg2

def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о вакансиях и компаниях-работодателях."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                vacancy_name VARCHAR(255),
                vacancy_url VARCHAR(255),
                area_id INTEGER,
                area_name VARCHAR(50),
                experience TEXT,
                description TEXT,
                salary_from INTEGER,
                salary_to INTEGER,
                salary_currency VARCHAR(50),
                company_id INTEGER
                CONSTRAINT fk_vacancies_companies
                FOREIGN KEY (company_id) REFERENCES companies (company_id) ON DELETE CASCADE
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE companies (
                company_id INTEGER PRIMARY KEY,
                company_name VARCHAR(255)
            )
        """)

    conn.commit()
    conn.close()

    print(f"БД {database_name} успешно создана")

