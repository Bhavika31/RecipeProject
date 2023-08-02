import sqlite3
import requests

def clear_data():
    # Connect to the database
    connection = sqlite3.connect("mealsdb")
    cursor = connection.cursor()

    # Delete all data from the 'ingredients' table
    cursor.execute("DELETE FROM ingredients")

    # Delete all data from the 'meals' table
    cursor.execute("DELETE FROM meals")

    # Delete all data from the 'meal_ingredients' table
    cursor.execute("DELETE FROM meal_ingredients")

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

def insert_data_from_api(meal_id):
    # Make the API request
    url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data directly from the response
        data = response.json()

        # Check if there are meals in the response
        if data and 'meals' in data and data['meals']:
            meal = data['meals'][0]  # Assuming there is only one meal in the response

            # Extract meal details
            meal_name = meal['strMeal']
            category = meal['strCategory']
            area = meal['strArea']
            instructions = meal['strInstructions']
            meal_thumb = meal['strMealThumb']
            tags = meal['strTags']
            youtube_link = meal['strYoutube']

            # Connect to the database
            connection = sqlite3.connect('mealsdb')
            cursor = connection.cursor()

            # Insert meal information into the 'meals' table
            insert_meal_query = "INSERT INTO meals (meal_id, meal_name, category, area, instructions, meal_thumb, tags, youtube_link) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            meal_values = (meal_id, meal_name, category, area, instructions, meal_thumb, tags, youtube_link)
            cursor.execute(insert_meal_query, meal_values)

            # Get the meal_id of the inserted meal
            meal_id = cursor.lastrowid

            # Extract ingredients and measurements and insert them into the 'ingredients' and 'meal_ingredients' tables
            for i in range(1, 21):
                ingredient = meal[f'strIngredient{i}']
                measurement = meal[f'strMeasure{i}']
                if ingredient and measurement:
                    # Convert ingredient name to lowercase for case-insensitive comparison
                    ingredient_lower = ingredient.lower()

                    # Check if the ingredient already exists in the 'ingredients' table
                    find_ingredient_query = "SELECT ingredient_id FROM ingredients WHERE LOWER(ingredient_name) = ?"
                    cursor.execute(find_ingredient_query, (ingredient_lower,))
                    existing_ingredient = cursor.fetchone()
                    if existing_ingredient:
                        # Ingredient already exists, use its ingredient_id
                        ingredient_id = existing_ingredient[0]
                    else:
                        # Insert ingredient into the 'ingredients' table
                        insert_ingredient_query = "INSERT INTO ingredients (ingredient_name) VALUES (?)"
                        ingredient_values = (ingredient,)
                        cursor.execute(insert_ingredient_query, ingredient_values)
                        # Get the ingredient_id of the inserted ingredient
                        ingredient_id = cursor.lastrowid

                    # Check if the meal-ingredient association already exists in the 'meal_ingredients' table
                    find_meal_ingredient_query = "SELECT * FROM meal_ingredients WHERE meal_id = ? AND ingredient_id = ?"
                    cursor.execute(find_meal_ingredient_query, (meal_id, ingredient_id))
                    existing_meal_ingredient = cursor.fetchone()
                    if not existing_meal_ingredient:
                        # Insert meal-ingredient association into the 'meal_ingredients' table
                        insert_meal_ingredient_query = "INSERT INTO meal_ingredients (meal_id, ingredient_id, measurement) VALUES (?, ?, ?)"
                        meal_ingredient_values = (meal_id, ingredient_id, measurement)
                        cursor.execute(insert_meal_ingredient_query, meal_ingredient_values)

            # Commit the changes and close the connection
            connection.commit()
            connection.close()

            print(f"Data for meal ID {meal_id} successfully added to the database.")
        else:
            print(f"No meal data found for meal ID {meal_id}.")
    else:
        print(f"Error: Unable to fetch data from the API for meal ID {meal_id}. Status Code: {response.status_code}")

# Clear existing data from the tables
clear_data()

for meal_id in range(52764, 53070):  # Adjust the range based on your desired meal IDs
    insert_data_from_api(meal_id)
