import psycopg2
import sqlite3
from config import pass2

def create_bd():
    conn = psycopg2.connect( user="postgres", password="123st321", host="127.0.0.1", port="5432")
    conn.autocommit=True
    cur = conn.cursor()
    cur.execute('CREATE DATABASE vkinder;')
    try:
        if psycopg2.connect(database="vkinder", user="postgres", password="123st321", host="127.0.0.1", port="5432"):
            print ( 'Создана база на локальном сервере : vkinder')
    except: print('Произошла ошибка база не создана')

def clear():
    ''' Удаление таблиц'''
    print('-' * 20, 'Подготовка', '-' * 20)

    conn = psycopg2.connect(database="vkinder", user="postgres", password="123st321", host="127.0.0.1", port="5432")

    cur = conn.cursor()
    with conn.cursor() as cur:
        cur.execute('''
                    SELECT table_name FROM information_schema.tables
                     WHERE table_schema NOT IN ('information_schema','pg_catalog');
                    ''')

        print('Были таблицы: ', cur.fetchall())

        cur.execute('DROP TABLE users CASCADE ')
        cur.execute('DROP TABLE  offer CASCADE')
        cur.execute('DROP TABLE  favorit CASCADE')
        cur.execute('DROP TABLE  black_list CASCADE')

        cur.execute('''
        SELECT table_name FROM information_schema.tables
        WHERE table_schema NOT IN ('information_schema','pg_catalog');
        ''')
        if cur.fetchall() == []:
            print('Все таблицы удалены')
        print()

def create_structure():

    '''Функция, создающая структуру БД (таблицы)'''
    conn = psycopg2.connect(database="vkinder", user="postgres", password='123st321', host="127.0.0.1", port="5432")

    conn.autocommit=False

    cur = conn.cursor()
    with conn.cursor() as cur:
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS users(user_id SERIAL PRIMARY KEY,
                                                                name VARCHAR(70),
                                                                age VARCHAR(30),
                                                                male VARCHAR(10), 
                                                                city VARCHAR(20)
                                                                );''')

            cur.execute('''CREATE TABLE IF NOT EXISTS offer(offer_id SERIAL PRIMARY KEY,
                                                                    user_id  INT REFERENCES users(user_id),
                                                                    name VARCHAR(70),
                                                                    age VARCHAR(30),
                                                                    male VARCHAR(10), 
                                                                    city VARCHAR(20),
                                                                    foto VARCHAR(150)

                                                                    );''')

            cur.execute('''CREATE TABLE IF NOT EXISTS favorit(favorit_id SERIAL PRIMARY KEY,
                                                                        user_id  INT REFERENCES users(user_id),
                                                                        offer_id INT REFERENCES offer(offer_id)
                                                                        );''')

            cur.execute('''CREATE TABLE IF NOT EXISTS black_list(black_list_id SERIAL PRIMARY KEY,
                                                                            user_id  INT REFERENCES users(user_id),
                                                                            offer_id INT REFERENCES offer(offer_id)
                                                                            );''')

            (cur.execute(''' SELECT * FROM users'''))
            conn.commit()

        except Exception:
            print('Что то пошло не так ')

        finally:
            print('Созданы таблицы для БД :', end=' ')

        cur.execute('''
                    SELECT table_name FROM information_schema.tables
                     WHERE table_schema NOT IN ('information_schema','pg_catalog');
                    ''')

        print(*cur.fetchall())
        print()



if __name__ == '__main__':
    create_bd()
    create_structure()

    # with psycopg2.connect(database='VKinder_db', user='postgres', password='postgres') as con:
    #
    #     create_structure(con)

