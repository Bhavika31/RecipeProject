import sqlite3

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

        category = int 

    # Create a query to search for recipes containing any of the input ingredients
    query = """
    SELECT m.meal_name, m.category, m.area, m.instructions, 
           m.youtube_link, m.tags, m.meal_thumb, 
           i.ingredient_name, mi.measurement
    FROM meals m
    JOIN meal_ingredients mi ON m.meal_id = mi.meal_id
    JOIN ingredients i ON mi.ingredient_id = i.ingredient_id
    WHERE LOWER(i.ingredient_name) IN ({})
    """.format(', '.join('?' for _ in input_ingredients))

    # Execute the query for input ingredients and retrieve matching recipes
    recipes = cursor.execute(query, input_ingredients).fetchall()

    # Close the connection
    connection.close()






    # Display the matching recipes and their ingredients
    if recipes:
        current_recipe_name = ""
        for recipe in recipes:
            if recipe[0] != current_recipe_name:
                current_recipe_name = recipe[0]
                print("Recipe Name:", recipe[0])
                print("Category:", recipe[1])
                print("Area:", recipe[2])
                print("Instructions:", recipe[3])
                print("Youtube Link:", recipe[4])
                print("Tags:", recipe[5])
                print("Meal Thumbnail:", recipe[6])
                print("Ingredients:")
            print(f"  - {recipe[7]}: {recipe[8]}")
            print("-" * 55)
            print()  # Add a new line between meals

    else:
        print("No recipes found with the provided ingredients.")

# Call the function to search for recipes by ingredients
search_recipes_by_ingredients()
