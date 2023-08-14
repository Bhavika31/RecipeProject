import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from collections import defaultdict
from urllib.parse import urlparse
import bcrypt
import datetime


app = Flask(__name__)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def search_recipes_by_ingredients(input_ingredients, category=None, area=None):
    try:
            # Connect to the database
            connection = sqlite3.connect('mealsdb')
            cursor = connection.cursor()

            # Convert the input ingredients to lowercase
            input_ingredients = [ingredient.strip().lower() for ingredient in input_ingredients]

            # Construct the SQL query with optional category and area filters
            query = """
            SELECT m.meal_name, m.category, m.area, m.instructions, 
                m.youtube_link, m.tags, m.meal_thumb, 
                i.ingredient_name, mi.measurement
            FROM meals m
            JOIN meal_ingredients mi ON m.meal_id = mi.meal_id
            JOIN ingredients i ON mi.ingredient_id = i.ingredient_id
            WHERE LOWER(i.ingredient_name) IN ({})
            {category_filter}
            {area_filter}
            ORDER BY m.meal_name
            """.format(
                ', '.join('?' for _ in input_ingredients),
                category_filter=f"AND m.category = '{category}'" if category else "",
                area_filter=f"AND m.area = '{area}'" if area else ""
            )

            # Execute the query with input ingredients and optional filters, and retrieve matching recipes
            recipes = cursor.execute(query, input_ingredients).fetchall()


            # Create a dictionary to store the recipe details and their ingredients
            recipe_details = defaultdict(lambda: {'name': '', 'category': '', 'area': '', 'instructions': '', 'youtube_link': '',
                                                'tags': '', 'meal_thumb': '', 'input_ingredients': [], 'remaining_ingredients': []})

            # Loop through the recipes and organize them in the 'recipe_details' dictionary
            for recipe in recipes:
                meal_name = recipe[0]
                if not recipe_details[meal_name]['name']:
                    # If recipe details are not already set for this recipe, update them
                    recipe_details[meal_name]['name'] = recipe[0]
                    recipe_details[meal_name]['category'] = recipe[1]
                    recipe_details[meal_name]['area'] = recipe[2]
                    recipe_details[meal_name]['instructions'] = recipe[3]
                    recipe_details[meal_name]['youtube_link'] = recipe[4] if is_valid_url(recipe[4]) else None
                    recipe_details[meal_name]['tags'] = recipe[5]
                    recipe_details[meal_name]['meal_thumb'] = recipe[6]

                # Append the ingredient and its measurement to the list of input ingredients for this recipe
                recipe_details[meal_name]['input_ingredients'].append((recipe[7], recipe[8]))

            # Create a dictionary to store the remaining ingredients for each recipe
            remaining_ingredients_dict = defaultdict(list)

            # Loop through the recipes and organize the remaining ingredients
            for recipe in recipes:
                meal_name = recipe[0]
                # Get the remaining ingredients for this recipe
                remaining_query = """
                SELECT i.ingredient_name, mi.measurement
                FROM meals m
                JOIN meal_ingredients mi ON m.meal_id = mi.meal_id
                JOIN ingredients i ON mi.ingredient_id = i.ingredient_id
                WHERE m.meal_name = ?
                AND i.ingredient_name NOT IN ({})
                """.format(', '.join('?' for _ in recipe_details[meal_name]['input_ingredients']))

                # Convert the zip object to a list before passing it to the execute function
                remaining_ingredients = cursor.execute(remaining_query, [meal_name, *list(zip(*recipe_details[meal_name]['input_ingredients']))[0]]).fetchall()

                # Add the remaining ingredients to the dictionary
                remaining_ingredients_dict[meal_name] = remaining_ingredients

            # Update the 'recipe_details' dictionary with remaining ingredients for each recipe
            for recipe_name, details in recipe_details.items():
                details['remaining_ingredients'] = remaining_ingredients_dict[recipe_name]

            # Close the database connection
            connection.close()

            # Return the recipe details as a list of dictionaries
            return list(recipe_details.values())
    
    except sqlite3.Error as e:
        # Handle database-related errors
        return f"Error accessing the database: {str(e)}"

    except Exception as e:
        # Handle other unexpected errors
        return f"An unexpected error occurred: {str(e)}"


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        ingredients = request.form.get('ingredients').split(',')
        category = request.form.get('category')
        area = request.form.get('area')
        recipes = search_recipes_by_ingredients(ingredients, category, area)
        return render_template('index.html', recipes=recipes)
    return render_template('index.html', recipes=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            # Connect to the database
            connection = sqlite3.connect('registration.db')
            cursor = connection.cursor()

            # Insert the user data into the 'users' table
            insert_query = """
            INSERT INTO users (username, password, email, registration_date)
            VALUES (?, ?, ?, ?)
            """
            cursor.execute(insert_query, (username, hashed_password, email, datetime.datetime.now()))

            # Commit the changes and close the connection
            connection.commit()
            connection.close()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        
        except sqlite3.Error as e:
            flash(f"Error registering user: {str(e)}", 'error')
            return redirect(url_for('register'))
        
        except Exception as e:
            flash(f"An unexpected error occurred: {str(e)}", 'error')
            return redirect(url_for('register'))

    return render_template('registration_file.html')  


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            # Connect to the database
            connection = sqlite3.connect('registration.db')
            cursor = connection.cursor()

            # Retrieve hashed password for the provided username
            query = "SELECT password FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            stored_password = cursor.fetchone()

            if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password[0]):
                # Passwords match, user is authenticated
                flash('Logged in successfully!', 'success')
                return redirect(url_for('protected_page'))
            else:
                # Incorrect username or password
                flash('Invalid username or password', 'error')
                return redirect(url_for('login'))
        except sqlite3.Error as e:
            flash(f"Error accessing the database: {str(e)}", 'error')
            return redirect(url_for('login'))
        finally:
            connection.close()

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
