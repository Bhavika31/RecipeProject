import sqlite3

def recipe_details(meal_id):
    try:
        # Replace 'mealsdb' with your actual database file name
        with sqlite3.connect('mealsdb') as conn:
            cursor = conn.cursor()

            # Fetch recipe details from the database using the recipe_id
            cursor.execute('SELECT * FROM meals WHERE meal_id = ?', (meal_id,))
            recipe = cursor.fetchone()

            if recipe:
                # Create a dictionary to hold the recipe details
                recipe_details = {
                    'name': recipe[1],
                    'category': recipe[2],
                    'area': recipe[3],
                    'instructions': recipe[4],
                    'tags': recipe[5],
                    'meal_thumb': recipe[6],
                    'meal_id': recipe[0]
                }

                # Fetch input ingredients for the recipe
                cursor.execute('''
                    SELECT i.ingredient_name, mi.measurement
                    FROM meal_ingredients mi
                    JOIN ingredients i ON mi.ingredient_id = i.ingredient_id
                    WHERE mi.meal_id = ?
                ''', (meal_id,))
                input_ingredients = cursor.fetchall()

                # Fetch remaining ingredients for the recipe
                cursor.execute('''
                    SELECT i.ingredient_name, mi.measurement
                    FROM meal_ingredients mi
                    JOIN ingredients i ON mi.ingredient_id = i.ingredient_id
                    WHERE mi.meal_id = ? AND i.ingredient_name NOT IN ({})
                '''.format(', '.join('?' for _ in input_ingredients)),
                (meal_id, *list(zip(*input_ingredients))[0]))
                remaining_ingredients = cursor.fetchall()

                # Organize ingredients data into the recipe_details dictionary
                recipe_details['input_ingredients'] = input_ingredients
                recipe_details['remaining_ingredients'] = remaining_ingredients

                # Fetch reviews for the recipe
                cursor.execute('SELECT * FROM ratings WHERE meal_id = ?', (meal_id))
                reviews = cursor.fetchall()

                # Calculate average rating
                total_rating = sum(review[4] for review in reviews)
                average_rating = total_rating / len(reviews) if len(reviews) > 0 else 0

                conn.close()

                return {
                    'recipe_details': recipe_details,
                    'reviews': reviews,
                    'average_rating': average_rating,
                    'num_reviews': len(reviews)
                }
            else:
                return "Recipe not found."

    except sqlite3.Error as e:
        return f"Error accessing the database: {str(e)}"

    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

if __name__ == "__main__":
    # Replace 'your_meal_id_here' with the actual meal_id you want to test
    test_meal_id = 52764
    result = recipe_details(test_meal_id)
    print(result)
