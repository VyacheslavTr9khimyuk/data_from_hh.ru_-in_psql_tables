import psycopg2

class DBManager:
    """
    Подключается к БД PostgreSQL и получает данные на запросы
    """
    def __init__(self, database_name, params):
        self.conn = psycopg2.connect(dbname=database_name, **params)


    def get_connect(self, sqrl):
        '''
        Обеспечивает связь с базой данных и реализует запрос с psql
        '''
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(sqrl)
                    self.conn.commit()
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()


    def get_union_table(self):
        '''
        Возвращает строку с кодом sql, который объединяет таблицы vacancies и companies. В таблице вакансий пересчитывает
        зарплату на рубли и находит среднее, если указана вилка
        '''
        sqrl_union = '''CREATE OR REPLACE VIEW vacancy_company_data AS
        SELECT v.vacancy_id vac_id, v.vacancy_name vac_name, v.salary_avg, v.vacancy_url vac_url,
        c.company_id comp_id, c.company_name comp_name
        FROM 
        (
        WITH a AS (
        SELECT *, 
        (CASE
            WHEN salary_currency = 'RUR' THEN salary_from
    	    WHEN salary_currency = 'EUR' THEN salary_from * 82
    	    WHEN salary_currency = 'USD' THEN salary_from * 72
        END) salary_from_RUR,
        (CASE
    	    WHEN salary_currency = 'RUR' THEN salary_to
    	    WHEN salary_currency = 'EUR' THEN salary_to * 82
    	    WHEN salary_currency = 'USD' THEN salary_to * 72
        END) salary_to_RUR
        FROM vacancies
        )
        SELECT vacancy_id, vacancy_name, company_id,
        (CASE
    	    WHEN salary_from_RUR IS NOT NULL AND salary_to_RUR IS NOT NULL THEN (salary_to_RUR + salary_from_RUR) / 2
    	    WHEN salary_from_RUR IS NOT NULL AND salary_to_RUR IS NULL THEN salary_from_RUR
    	    WHEN salary_from_RUR IS NULL AND salary_to_RUR IS NOT NULL THEN salary_to_RUR
        END) salary_avg
        FROM a
        ) v
        JOIN
        (
        SELECT company_id, company_name
        FROM companies
        GROUP BY company_id, company_name
        ) c
        ON c.company_id = v.company_id
        ORDER BY v.vacancy_id;
        '''
        return sqrl_union


    def get_companies_and_vacancies_count(self):
        """
        получает список всех компаний и количество вакансий у каждой компании.
        :return:
        """
        sqrl_union = self.get_union_table()
        sqrl_response = '''SELECT DISTINCT c.company_name, COUNT(v.vacancy_id)
        FROM vacancy_company_data;
        '''
        sqrl = f"{sqrl_union} {sqrl_response}"
        self.get_connect(sqrl)


    def get_all_vacancies(self):
        """
        получает список всех вакансий с указанием названия компании, названия
        вакансии и зарплаты и ссылки на вакансию.
        """
        sqrl_union = self.get_union_table()
        sqrl_response = '''SELECT c.company_name, v.vacancy_name, v.salary_avg, v.vacancy_url 
        FROM vacancy_company_data;
        '''
        sqrl = f"{sqrl_union} {sqrl_response}"
        self.get_connect(sqrl)


    def get_avg_salary(self):
        """
        получает среднюю зарплату по вакансиям.
        """
        sqrl_union = self.get_union_table()
        sqrl_response = '''SELECT AVG(v.salary_avg)
        FROM vacancy_company_data;
        '''
        sqrl = f"{sqrl_union} {sqrl_response}"
        self.get_connect(sqrl)


    def get_vacancies_with_higher_salary(self):
        """
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        sqrl_union = self.get_union_table()
        sqrl_response = '''SELECT *
        FROM vacancy_company_data
        WHERE v.salary_avg > AVG(v.salary_avg);
        '''
        sqrl = f"{sqrl_union} {sqrl_response}"
        self.get_connect(sqrl)


    def get_vacancies_with_keyword(self, word):
        """
        получает список всех вакансий, в названии которых содержатся переданные в метод
        слова, например python.
        :return:
        """
        sqrl_union = self.get_union_table()
        sqrl_response = '''SELECT *
        FROM vacancy_company_data
        WHERE word IN (v.vacancy_name);
        '''
        sqrl = f"{sqrl_union} {sqrl_response}"
        self.get_connect(sqrl)
