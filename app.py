from flask import Flask, render_template, request, redirect,flash, session, url_for
import sqlite3
import re
import bcrypt
from datetime import datetime
from collections import defaultdict
from urllib.parse import urlparse

from get_meal import is_valid_url, search_recipes_by_ingredients

app = Flask(__name__)
app.secret_key = '1'


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    try:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']

            with sqlite3.connect('mealsdb') as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
                account = cursor.fetchone()

            if not username or not password:
                msg = 'Please fill in all details!'
            elif account and bcrypt.checkpw(password.encode('utf-8'), account[2]):
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                msg = 'Logged in successfully!'
                return redirect(url_for('home'))
            else:
                msg = 'Incorrect username / password!'

            conn.close()
        return render_template('login.html', msg=msg)
    except Exception as e:
        msg = 'Error: {}'.format(str(e))
        return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    try:
        if request.method == 'POST':
            username = request.form['username']
            raw_password = request.form['password']
            email = request.form['email']

            if not username or not raw_password or not email:
                msg = 'Please fill in all details!'
            else:
                hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())

                with sqlite3.connect('mealsdb') as conn:
                    cursor = conn.cursor()
                    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
                    account = cursor.fetchone()

                if account:
                    msg = 'Account already exists!'
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    msg = 'Invalid email address!'
                elif not re.match(r'[A-Za-z0-9]+', username):
                    msg = 'Username must contain only characters and numbers!'
                else:
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    with sqlite3.connect('mealsdb') as conn:
                        cursor = conn.cursor()
                        cursor.execute('INSERT INTO users (username, password, email, registration_date) VALUES (?, ?, ?, ?)',
                                       (username, hashed_password, email, current_time))
                        conn.commit()
                    
                    msg = 'You have successfully registered!'
                 
    except Exception as e:
        msg = 'Error: {}'.format(str(e))
    
    finally:
        conn.close()
    
    return render_template('registration_file.html', msg=msg)

@app.route('/logout')
def logout():
    # clears the session data
    session.clear()
    return redirect(url_for('home'))

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        ingredients = request.form.get('ingredients').split(',')
        category = request.form.get('category')
        cuisine = request.form.get('cuisine')
        recipes = search_recipes_by_ingredients(ingredients, category, cuisine)
        return render_template('index.html', recipes=recipes)

    return render_template('index.html', recipes=None)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/submit_review/<int:meal_id>', methods=['POST'])
def submit_review(meal_id):
    try:
        # Retrieve form data: rating and feedback
        rating = int(request.form['rating'])
        feedback = request.form['feedback']

        # Get user_id and username from the session
        user_id = session.get('id')
        username = session.get('username')

        # Create a UTC timestamp using datetime.utcnow()
        timestamp = datetime.utcnow()

        # Insert the review into the ratings table
        with sqlite3.connect('mealsdb') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO ratings (user_id, username, meal_id, rating, feedback, time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, username, meal_id, rating, feedback, timestamp))
            conn.commit()
            
            return redirect(url_for('recipe_details', meal_id=meal_id))
        
    except sqlite3.Error as e:
        error_msg = f"SQLite error: {str(e)}"
        return render_template('error.html', error_msg=error_msg)

    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"

    finally:
        conn.close()
    
    return render_template('error.html', error_msg=error_msg)

@app.route('/review_form/<int:meal_id>', methods=['GET'])
def review_form(meal_id):
    # Check if the user is logged in
    if 'loggedin' not in session or not session['loggedin']:
        flash('Please log in to add a review.', 'error')
        return redirect(url_for('recipe_details', meal_id=meal_id))

    return render_template('review_form.html', meal_id=meal_id)

@app.route('/recipe_details/<int:meal_id>')
def recipe_details(meal_id):
    try:
        # Fetch detailed recipe information from the database
        with sqlite3.connect('mealsdb') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM meals WHERE meal_id = ?', (meal_id,))
            recipe = cursor.fetchone()

            # Fetch reviews for the recipe
            cursor.execute('SELECT * FROM ratings WHERE meal_id = ?', (meal_id,))
            reviews = cursor.fetchall()

            # Calculate average rating
            total_rating = sum(review[4] for review in reviews)
            average_rating = total_rating / len(reviews) if len(reviews) > 0 else 0

            # Fetch all ingredients for the recipe
            cursor.execute('''
                SELECT i.ingredient_name, mi.measurement
                FROM meal_ingredients mi
                JOIN ingredients i ON mi.ingredient_id = i.ingredient_id
                WHERE mi.meal_id = ?
            ''', (meal_id,))
            ingredients = cursor.fetchall()

        
        return render_template(
            'recipe_details.html',
            recipe=recipe,
            reviews=reviews,
            ingredients=ingredients,
            average_rating=average_rating,
            num_reviews=len(reviews),
            meal_id=meal_id
        )

    except sqlite3.Error as e:
        return f"Error accessing the database: {str(e)}"

    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
    
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(host='127.0.0.1')
