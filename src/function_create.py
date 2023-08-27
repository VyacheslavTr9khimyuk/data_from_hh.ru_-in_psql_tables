import psycopg2

def create_database(db_vacancies: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о вакансиях и компаниях-работодателях."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {db_vacancies}")
    cur.execute(f"CREATE DATABASE {db_vacancies}")

    conn.close()

    conn = psycopg2.connect(dbname=db_vacancies, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                name VARCHAR(255),
                experience TEXT,
                description TEXT,
                salary_from INTEGER,
                salary_to INTEGER,
                salary_currency VARCHAR(50)
                company_id INTEGER
                CONSTRAINT fk_vacancies_companies
                FOREIGN KEY (company_id) REFERENCES companies (company_id) ON DELETE CASCADE
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE companies (
                company_id INTEGER PRIMARY KEY,
                name VARCHAR(255),

            )
        """)

    conn.commit()
    conn.close()