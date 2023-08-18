import unittest
from get_meal import search_recipes_by_ingredients
import pytest
from unittest.mock import patch
from app import app

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
        type_recipes = search_recipes_by_ingredients(type_ingredients)
        self.assertTrue(type_recipes)

        
        # Test case 5: Ingredients with special characters and numbers
        special_ingredients = ['@chicken', '5-rice']
        special_recipes = search_recipes_by_ingredients(special_ingredients)
        self.assertFalse(special_recipes)

        # Test case 6: Search with a single ingredient
        single_ingredient = ['beef']
        single_ingredient_recipes = search_recipes_by_ingredients(single_ingredient)
        self.assertTrue(single_ingredient_recipes)

        # Test case 7: Search with specific ingredients that should match exactly
        exact_ingredients = ['bread flour', 'ground beef']
        exact_recipes = search_recipes_by_ingredients(exact_ingredients)
        self.assertTrue(exact_recipes)

        # Test case 8: Search with a long list of ingredients
        long_ingredients = ['chicken', 'rice', 'onion', 'garlic', 'bell pepper', 'tomato', 'lettuce']
        long_recipes = search_recipes_by_ingredients(long_ingredients)
        self.assertTrue(long_recipes)


def test_submit_review_invalid_rating(self):
    # Test invalid review rating (not an integer)
    response = self.client.post('/submit_review/1', data={'rating': 'abc', 'feedback': 'Invalid rating!'})
    assert b'Invalid rating format.' in response.data

def test_submit_review_missing_feedback(self):
    # Test submitting a review without feedback
    response = self.client.post('/submit_review/1', data={'rating': 4, 'feedback': ''})
    assert b'Please provide feedback.' in response.data


    def test_submit_review_invalid_meal_id(self):
        # Test submitting a review for a non-existing meal ID
        response = client.post('/submit_review/999', data={'rating': 4, 'feedback': 'Invalid meal ID!'})
        assert b'Meal not found.' in response.data

    def test_review_form_authenticated(self):
        # Test accessing the review form while authenticated
        with client.session_transaction() as session:
            session['loggedin'] = True
            session['id'] = 1
            session['username'] = 'test_user'
        response = client.get('/review_form/1')
        assert b'<form id="review-form" method="post">' in response.data

def test_review_form_unauthenticated(self):
    # Test accessing the review form while unauthenticated
    response = client.get('/review_form/1')
    assert b'Please log in to add a review.' in response.data

def test_about_route(self):
    # Test the about route content
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About Us' in response.data

def test_recipe_details_valid_id(self):
    # Test recipe details for a valid meal ID
    response = client.get('/recipe_details/1')
    assert response.status_code == 200
    assert b'Recipe Details' in response.data

def test_recipe_details_invalid_id(self):
    # Test recipe details for a non-existing meal ID
    response = client.get('/recipe_details/999')
    assert response.status_code == 404
    assert b'Meal not found.' in response.data

def test_recipe_details_valid_id_with_reviews(self):
    # Test recipe details for a valid meal ID with existing reviews
    response = client.get('/recipe_details/1')
    assert b'Average Rating' in response.data

def test_recipe_details_valid_id_no_reviews(self):
    # Test recipe details for a valid meal ID without reviews
    response = client.get('/recipe_details/2')
    assert b'No reviews yet.' in response.data

def test_logout_route(self):
    # Test logging out clears the session
    with client.session_transaction() as session:
        session['loggedin'] = True
    response = client.get('/logout')
    assert 'loggedin' not in session
    assert response.status_code == 302
    assert response.location == 'http://localhost/'

def test_main_route_with_inputs(self):
    # Test the main route with various inputs
    response = client.post('/', data={
        'ingredients': 'chicken, rice',
        'category': 'Main Dish',
        'area': 'Italian'
    })
    assert b'Recipe Results' in response.data

def test_main_route_empty_inputs(self):
    # Test the main route with empty inputs
    response = client.post('/', data={})
    assert b'Recipe Results' in response.data

def test_successful_registration(client, register_fixture, register_url):
    response = client.post(register_url, data={'username': 'testuser', 'password': 'testpass', 'email': 'test@example.com'})
    assert b'You have successfully registered!' in response.data

def test_empty_registration_form(client, register_fixture, register_url):
    response = client.post(register_url, data={'username': '', 'password': '', 'email': ''})
    assert b'Please fill in all details!' in response.data

def test_registration_success(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'test@example.com'
    })
    assert response.status_code == 200
    assert b'You have successfully registered!' in response.data

def test_registration_missing_fields(client):
    response = client.post('/register', data={})
    assert response.status_code == 200
    assert b'Please fill in all details!' in response.data

def test_registration_existing_account(client):
    response = client.post('/register', data={
        'username': 'existinguser',
        'password': 'testpassword',
        'email': 'existing@example.com'
    })
    assert response.status_code == 200
    assert b'Account already exists!' in response.data

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_successful(client):
    response = client.post('/login', data={'username': 'valid_username', 'password': 'valid_password'})
    assert b'Logged in successfully!' in response.data

def test_login_invalid_credentials(client):
    response = client.post('/login', data={'username': 'invalid_username', 'password': 'invalid_password'})
    assert b'Incorrect username / password!' in response.data

def test_login_success(client):
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert b'Logged in successfully!' in response.data

def test_login_invalid_credentials(client):
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 200
    assert b'Incorrect username / password!' in response.data

def test_login_missing_fields(client):
    response = client.post('/login', data={})
    assert response.status_code == 200
    assert b'Please fill in all details!' in response.data


def test_submit_review_authenticated(client):
    with client.session_transaction() as session:
        session['loggedin'] = True
        session['id'] = 1
        session['username'] = 'test_user'
    
    response = client.post('/submit_review/1', data={'rating': 5, 'feedback': 'Great recipe!'})
    assert b'Review submitted successfully!' in response.data

def test_submit_review_unauthenticated(client):
    response = client.post('/submit_review/1', data={'rating': 5, 'feedback': 'Great recipe!'})
    assert b'Please log in to add a review.' in response.data

def test_submit_review_success(client):
    response = client.post('/submit_review/1', data={
        'rating': 5,
        'feedback': 'Great recipe!'
    })
    assert response.status_code == 200
    assert b'Review submitted successfully!' in response.data

def test_submit_review_missing_fields(client):
    response = client.post('/submit_review/1', data={})
    assert response.status_code == 200
    assert b'Please provide both rating and feedback.' in response.data



if __name__ == '__main__':
    unittest.main()


