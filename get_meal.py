import sqlite3
from collections import defaultdict
from urllib.parse import urlparse

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
        SELECT m.meal_id, m.meal_name, m.meal_thumb
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

        # Create a list to store the basic recipe details
        recipe_details_list = []

        # Loop through the recipes and organize the basic details
        for recipe in recipes:
            recipe_details_list.append({
                'meal_id': recipe[0],
                'name': recipe[1],
                'meal_thumb': recipe[2]
            })


        # Return the basic recipe details as a list of dictionaries
        return recipe_details_list

    except sqlite3.Error as e:
        # Handle database-related errors
        return f"Error accessing the database: {str(e)}"

    except Exception as e:
        # Handle other unexpected errors
        return f"An unexpected error occurred: {str(e)}"
    
    finally:
        connection.close()
