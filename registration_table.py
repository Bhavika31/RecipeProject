import sqlite3

def create_table():
    with sqlite3.connect('registration.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                registration_date TEXT NOT NULL
            )
        ''')

create_table()
