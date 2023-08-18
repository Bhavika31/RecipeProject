import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import register

# Mock SQLite database using SQLite in-memory
app = Flask(__name__)
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def app_context():
    with app.app_context():
        yield db

@pytest.fixture
def register_url():
    return '/register'

# Provide the fixtures needed for your tests
@pytest.fixture
def register_fixture(client, app_context, register_url):
    return register



