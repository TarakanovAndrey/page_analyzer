import psycopg2
from psycopg2 import Error, extras
from dotenv import load_dotenv
import os


load_dotenv()

db = os.getenv('DATABASE_URL')


def insert_checks_result(id_, checks_result):
    status_code = checks_result['status_code']
    h1 = checks_result['h1']
    title = checks_result['title']
    description = checks_result['description']

    query = (f'''INSERT INTO url_checks (url_id, status_code, h1, title, description)
            VALUES ({id_}, {status_code}, '{h1}', '{title}', '{description}');''')

    with psycopg2.connect(db) as connect:
        try:
            cursor = connect.cursor()
            cursor.execute(query)

        except (Exception, Error) as error:
            print("Ошибка при работе с Postgresql", error)


def insert_url(url):

    query = f"INSERT INTO urls (name) VALUES ('{url}') ON CONFLICT (name) DO NOTHING RETURNING id;"

    with psycopg2.connect(db) as connect:
        try:
            cursor = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(query)
            id_new_row = cursor.fetchone()[0]
            return id_new_row
        except (Exception, Error) as error:
            print("Ошибка при работе с Postgresql", error)


def get_id(url):

    query = f"SELECT id FROM urls WHERE name='{url}'"

    with psycopg2.connect(db) as connect:
        try:
            cursor = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(query)
            return cursor.fetchone()['id']
        except (Exception, Error) as error:
            print("Ошибка при работе с Postgresql", error)


def get_url_info(id_note):

    query = f"SELECT id, name, DATE(created_at) FROM urls WHERE id='{id_note}'"

    with psycopg2.connect(db) as connect:
        try:
            cursor = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(query)
            return cursor.fetchone()
        except (Exception, Error) as error:
            print("Ошибка при работе с Postgresql", error)


def get_sites_url(id_note):

    query = f"SELECT name FROM urls WHERE id='{id_note}'"

    with psycopg2.connect(db) as connect:
        try:
            cursor = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(query)
            return cursor.fetchone()['name']
        except (Exception, Error) as error:
            print("Ошибка при работе с Postgresql", error)


def get_checks_info_of_url(id_note):

    query = f'''SELECT id, status_code, h1, title, description, DATE(created_at)
            FROM url_checks
            WHERE url_id='{id_note}'
            ORDER BY id DESC'''

    with psycopg2.connect(db) as connect:
        try:
            cursor = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(query)
            return cursor.fetchall()
        except (Exception, Error) as error:
            print("Ошибка при работе с Postgresql", error)


def check_urls_exist(url: str):

    query = f"SELECT EXISTS (SELECT name FROM urls WHERE name='{url}');"

    with psycopg2.connect(db) as connect:
        try:
            cursor = connect.cursor()
            cursor.execute(query)
            rows = cursor.fetchone()
            return rows[0]
        except (Exception, Error) as error:
            print("Ошибка при работе с Postgresql", error)


def get_urls_info():
    query = "SELECT id, name FROM urls ORDER BY id DESC"
    with psycopg2.connect(db) as connect:
        try:
            cursor = connect.cursor(cursor_factory=extras.DictCursor)
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except (Exception, Error) as error:
            print("Ошибка при работе с Postgresql", error)


def get_checks_info():
    query = '''SELECT url_id, status_code, MAX(DATE(created_at))
               FROM url_checks GROUP BY url_id, status_code
               ORDER BY url_id DESC;'''

    with psycopg2.connect(db) as connect:
        try:
            cursor = connect.cursor(cursor_factory=extras.DictCursor)
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except (Exception, Error) as error:
            print("Ошибка при работе с Postgresql", error)
