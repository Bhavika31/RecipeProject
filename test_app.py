import unittest
from app import search_recipes_by_ingredients

class TestApp(unittest.TestCase):
    def test_search_recipes_by_ingredients(self):
        # Test case 1: Provide a list of ingredients that should return some recipes
        ingredients = ["chicken", "rice"]
        recipes = search_recipes_by_ingredients(ingredients)
        self.assertTrue(recipes)  # Assert that there are recipes in the search results

        # Test case 2: Provide an empty list of ingredients that should return no recipes
        empty_ingredients = []
        empty_recipes = search_recipes_by_ingredients(empty_ingredients)
        self.assertFalse(empty_recipes)  # Assert that there are no recipes in the search results

        # Test the function when the input list contains ingredients that do not exist in the database.
        false_ingredients = ['kiwi', 'mango']
        false_recipes = search_recipes_by_ingredients(false_ingredients)
        self.assertFalse(false_recipes)

        #Test for upper and lower case inputs
        type_ingredients = ['MiLk', 'TOMATO']
        type_recipes = search_recipes_by_ingredients(type_ingredients_ingredients)
        self.assertTrue(type_recipes_recipes)


    
if __name__ == '__main__':
    unittest.main()


