import sqlite3
from collections import defaultdict

def search_recipes_by_ingredients():
    # Connect to the database
    connection = sqlite3.connect('mealsdb')
    cursor = connection.cursor()

    # Get user input for up to 10 ingredients
    input_ingredients = []
    for i in range(10):
        ingredient = input(f"Enter Ingredient {i + 1} (or type 'done' to stop): ").strip()
        if ingredient.lower() == 'done':
            break
        input_ingredients.append(ingredient.lower())

    query = """
    SELECT m.meal_name, m.category, m.area, m.instructions, 
           m.youtube_link, m.tags, m.meal_thumb, 
           i.ingredient_name, mi.measurement
    FROM meals m
    JOIN meal_ingredients mi ON m.meal_id = mi.meal_id
    JOIN ingredients i ON mi.ingredient_id = i.ingredient_id
    WHERE LOWER(i.ingredient_name) IN ({})
    ORDER BY m.meal_name
    """.format(', '.join('?' for _ in input_ingredients))

    # Execute the query for input ingredients and retrieve matching recipes
    recipes = cursor.execute(query, input_ingredients).fetchall()

    # Create a dictionary to store the recipe details and their ingredients
    recipe_details = defaultdict(lambda: {'name': '', 'category': '', 'area': '', 'instructions': '', 'youtube_link': '',
                                          'tags': '', 'meal_thumb': '', 'input_ingredients': []})

    # Loop through the recipes and organize them in the 'recipe_details' dictionary
    for recipe in recipes:
        meal_name = recipe[0]
        if not recipe_details[meal_name]['name']:
            # If recipe details are not already set for this recipe, update them
            recipe_details[meal_name]['name'] = recipe[0]
            recipe_details[meal_name]['category'] = recipe[1]
            recipe_details[meal_name]['area'] = recipe[2]
            recipe_details[meal_name]['instructions'] = recipe[3]
            recipe_details[meal_name]['youtube_link'] = recipe[4]
            recipe_details[meal_name]['tags'] = recipe[5]
            recipe_details[meal_name]['meal_thumb'] = recipe[6]

        # Append the ingredient and its measurement to the list of input ingredients for this recipe
        recipe_details[meal_name]['input_ingredients'].append((recipe[7], recipe[8]))

    # Loop through the 'recipe_details' dictionary and print the recipe information
    for recipe_name, details in recipe_details.items():
        print("Recipe Name:", details['name'])
        print("Category:", details['category'])
        print("Area:", details['area'])
        print("Instructions:", details['instructions'])
        print("Youtube Link:", details['youtube_link'])
        print("Tags:", details['tags'])
        print("Meal Thumbnail:", details['meal_thumb'])

        # Print the ingredients provided by the user
        print("Ingredients Provided:")
        for ingredient, measurement in details['input_ingredients']:
            print(f"  - {ingredient}: {measurement}")

        # Execute a separate query to get the remaining ingredients for this recipe
        remaining_query = """
        SELECT i.ingredient_name, mi.measurement
        FROM meals m
        JOIN meal_ingredients mi ON m.meal_id = mi.meal_id
        JOIN ingredients i ON mi.ingredient_id = i.ingredient_id
        WHERE m.meal_name = ?
        AND i.ingredient_name NOT IN ({})
        """.format(', '.join('?' for _ in details['input_ingredients']))

        # Convert the zip object to a list before passing it to the execute function
        remaining_ingredients = cursor.execute(remaining_query, [details['name'], *list(zip(*details['input_ingredients']))[0]]).fetchall()

        # Print the remaining ingredients and their respective measurements
        print("Remaining Ingredients:")
        for ingredient, measurement in remaining_ingredients:
            print(f"  - {ingredient}: {measurement}")

        print("-" * 55)
        print()  # Add a new line between meals

    if not recipe_details:
        print("No recipes found with the provided ingredients.")

    # Close the connection after processing all recipes
    connection.close()

# Call the function to search for recipes by ingredients
search_recipes_by_ingredients()
