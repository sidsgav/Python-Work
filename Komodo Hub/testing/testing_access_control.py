# * Gavin's Code *

# * Gavin starts coding here *

from newApp import app, db, User # Import necessary modules from the main application file
import pytest 

@pytest.fixture
def client():

    app.config['TESTING'] = True # Enable 'Flask' testing mode
    client = app.test_client() # Create a test client 
    with app.app_context():
        db.create_all() # Create respective tables in the in-memory database
        yield client 
        db.session.remove() # Clears the database session after each test is done
        db.drop_all() # This is done to clean the state for each test after preceding - *remember to remove after in all files *

def test_student_restrictions(client):

    student = User(username="student_user", # Create respective info regarding student user account
                   password="TestPass123", 
                   accountType="student")
    db.session.add(student) # Adds the student to the database
    db.session.commit()
    response = client.get('/teacher_dashboard', follow_redirects=True) # Attempt to access teacher dashboard
    assert response.status_code == 403 # Respective response for error code

def test_teacher_access(client):

    teacher = User(username="teacher_user", password="TestPass123", accountType="teacher") # Create a teacher user
    db.session.add(teacher) # Add the teacher data to the database
    db.session.commit() # Commits the changes
    response = client.get('/teacher_dashboard', follow_redirects=True) # Attempts to access teacher dashboard
    assert response.status_code == 200 # Successful access code 

"""" A public user test was not done as there are a few features not yet implemented so seemed pointless yet
     However, this was done to ensure each account type remained standalone and ensures public user account types
     will stay secure too considering the security enforecments we have taken """

# * Gavin stops coding here *