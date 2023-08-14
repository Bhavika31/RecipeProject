import sqlite3

def create_table():
    with sqlite3.connect('mealsdb') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ratings (
                rating_id INTEGER PRIMARY KEY NOT NULL,
                user_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                meal_id INTEGER NOT NULL,
                rating INTEGER,
                feedback TEXT,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (meal_id) REFERENCES meals(meal_id)
                        )
        ''')

create_table()
