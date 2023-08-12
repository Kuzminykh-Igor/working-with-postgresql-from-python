import psycopg2

def create_db(cur):
    '''Функция, создающая структуру БД (таблицы).'''
    cur.execute("""
         CREATE TABLE IF NOT EXISTS client (
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL
        );
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone (
            phone_id SERIAL PRIMARY KEY,
            phone VARCHAR(15) NULL,
            client_id INTEGER NOT NULL REFERENCES client(client_id)
        );
        """)
    conn.commit()

def add_client(cur, first_name, last_name, email, phone=None):
    '''Функция, позволяющая добавить нового клиента.'''
    cur.execute("""
        INSERT INTO client(first_name, last_name, email)
        VALUES(%s, %s, %s)
        RETURNING client_id;
        """, (first_name, last_name, email))
    client_id = cur.fetchone()
    if phone is not None:
        cur.execute("""
            INSERT INTO phone(client_id, phone)
            VALUES(%s, %s);
            """, (client_id, phone))
    conn.commit()

def add_phone(cur, client_id, phone):
    '''Функция, позволяющая добавить телефон для существующего клиента.'''
    cur.execute("""
        INSERT INTO phone(client_id, phone)
        VALUES(%s, %s);
        """, (client_id, phone))
    conn.commit()

def change_client(cur, client_id, first_name=None, last_name=None, email=None, phone=None):
    '''Функция, позволяющая изменить данные о клиенте.'''
    if first_name is not None:
        cur.execute("""
            UPDATE client SET first_name=%s
            WHERE client_id=%s;
            """, (first_name, client_id))
    if last_name is not None:
        cur.execute("""
            UPDATE client SET last_name=%s
            WHERE client_id=%s;
            """, (last_name, client_id))
    if email is not None:
        cur.execute("""
            UPDATE client SET email=%s
            WHERE client_id=%s;
            """, (email, client_id))
    if phone is not None:
        cur.execute("""
            UPDATE phone SET phone=%s
            WHERE client_id=%s;
            """, (phone, client_id))
    conn.commit()

def delete_phone(cur, client_id, phone):
    '''Функция, позволяющая удалить телефон для существующего клиента.'''
    cur.execute("""
        DELETE FROM phone
        WHERE client_id=%s AND phone=%s;
        """, (client_id, phone))
    conn.commit()

def delete_client(cur, client_id):
    '''Функция, позволяющая удалить существующего клиента.'''
    cur.execute("""
        DELETE FROM phone
        WHERE client_id=%s;
        """, (client_id,))
    cur.execute("""
        DELETE FROM client
        WHERE client_id=%s;
        """, (client_id,))
    conn.commit()

def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
    '''Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.'''
    if first_name is not None:
        cur.execute("""
            SELECT client_id
            FROM client
            WHERE first_name=%s;
            """, (first_name,))
    if last_name is not None:
        cur.execute("""
            SELECT client_id
            FROM client
            WHERE last_name=%s;
            """, (last_name,))
    if email is not None:
        cur.execute("""
            SELECT client_id
            FROM client
            WHERE email=%s;
            """, (email,))
    if phone is not None:
        cur.execute("""
            SELECT client_id
            FROM phone
            WHERE phone=%s;
            """, (phone,))
    id_client = cur.fetchone()
    cur.execute("""
        SELECT c.client_id, first_name, last_name, email, phone
        FROM client AS c
        LEFT JOIN phone AS p ON p.client_id = c.client_id
        WHERE c.client_id=%s;
        """, (id_client,))
    for person in cur.fetchall():
        print(person)
    print()


def delete_db(cur):
    '''Функция, удаляющая всю структуру БД (таблицы).'''
    cur.execute("""
    DROP TABLE phone;
    DROP TABLE client;
    """)


with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    with conn.cursor() as cur:

        # delete_db(cur)  # Функция, удаляющая всю структуру БД (таблицы).
        create_db(cur)

        add_client(cur, 'Nick', 'Nlte', 'n.nolte@gmail.com', 13102796312)
        add_client(cur, 'Robin', 'Williams', 'r.will@outlook.com')
        add_client(cur, 'Gary', 'Oldman', 'g.oldman@mail.ru')
        add_client(cur, 'Toy', 'Jones', 't.jones@yandex.ru', 79991237799)
        add_client(cur, 'Peter', 'Falk', 'peter.falk@rambler.ru')

        add_phone(cur, 1, 13108541111)
        add_phone(cur, 1, 13105691199)
        add_phone(cur, 3, 13108503770)

        change_client(cur, 4, first_name='Toby')
        change_client(cur, 1, last_name='Nolte')
        change_client(cur, 2, email='r.williams@outlook.com')
        change_client(cur, 4, phone=79991117799)

        delete_phone(cur, 1, '13105691199')

        delete_client(cur, 5)

        find_client(cur, first_name='Toby')
        find_client(cur, last_name='Nolte')
        find_client(cur, email='r.williams@outlook.com')
        find_client(cur, phone='13108503770')

conn.close()