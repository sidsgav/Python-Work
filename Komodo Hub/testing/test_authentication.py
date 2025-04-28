# * Gavin's Code *

# * Gavin starts coding here *

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/..")) # Finds 'newApp.py' file with absoloute path
from newApp import app, db  
from newApp import User  # Import the User model for testing
from werkzeug.security import check_password_hash # Security test

@pytest.fixture
def client():
    app.config['TESTING'] = True # Emulates a test client anf creates an in-memory database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Here is a temporary database for tests
    client = app.test_client()
    with app.app_context():
        db.create_all() # Create tables in test database
        yield client
        db.session.remove()
        db.drop_all() # Clean up after tests

def test_registration(client):
    inputVal = client.post('/register', data={ # Test the user's registration
        'username': 'testuser', # Inpute details[...]
        'password': 'Test1234',
        'accountType': 'student'}, 
        follow_redirects=True)
    user = User.query.filter_by(username="testuser").first()
    assert user is not None # Ensures the user is created
    assert check_password_hash(user.password, "Test1234") # Verify password hashing for utmost security implementation

# * Gavin stops coding here *
