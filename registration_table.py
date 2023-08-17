import sqlite3

def create_table():
    with sqlite3.connect('mealsdb') as conn:
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



def create_ratings_table():
    with sqlite3.connect('mealsdb') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ratings (
                rating_id INTEGER PRIMARY KEY NOT NULL,
                user_id INTEGER NOT NULL,
                username TEXT,
                meal_id INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                feedback TEXT,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (username) REFERENCES users(username),
                FOREIGN KEY (meal_id) REFERENCES meals(meal_id)
            )
        ''')

create_ratings_table()

