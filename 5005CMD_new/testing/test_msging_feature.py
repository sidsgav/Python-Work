# * Gavin's Code *

from newApp import app, db, Message, User
import pytest
from werkzeug.security import generate_password_hash # Import password hashing utility as this prevents test case pass (debug)

@pytest.fixture
def client():
    app.config['TESTING'] = True # Setting uo a test client with a standalone database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Again use an in-memory database for testing
    client = app.test_client()
    with app.app_context():
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()

def test_send_message(client):
    """ Test sending a message and ensuring it appears in recipient's inbox """
    with app.app_context():
        sender = User(username="sender", password=generate_password_hash("TestPassw0rd1234"), accountType="teacher") # User with hashed pass
        recipient = User(username="recipient", password=generate_password_hash("TestPassw0rd1234"), accountType="student") # Second user with hashed pass
        db.session.add(sender)
        db.session.add(recipient)
        db.session.flush() # Ensure the associated IDs are assigned before commited
        db.session.commit()
        print(f"Sender ID: {sender.id}, Recipient ID: {recipient.id}")

        loginVal = client.post('/login', data={ # Logs in the user before sending a message
            'username': sender.username,
            'password': "TestPassw0rd1234", # Plain text because hashing happens inside the login function
            'accountType': sender.accountType}, 
            follow_redirects=True)
        print(f"Login Validation Status: {loginVal.status_code}") # Check 1
        print(f"Login Validation Data: {loginVal.data.decode()}") # Check 2
        assert loginVal.status_code == 200, "Login failed" # Status repr if login fails
        with client.session_transaction() as session: # Simulates session as if user is loggedd in
            session["_user_id"] = sender.id # Simulating Flask-Login session
            session["_fresh"] = True # Marks session as fresh

        response = client.post('/messages/send', data={ # Sends a message once a session has started
            'recipientID': str(recipient.id), # Convert to a string
            'content': "This is a test message."}, 
            follow_redirects=True)
        print(f"Message Send Response Status: {response.status_code}")
        print(f"Message Send Response Data: {response.data.decode()}")

        db.session.flush() # Here I check the database
        db.session.commit() # ^
        all_messages = Message.query.all()
        print(f"All Messages in database: {all_messages}")
        message = Message.query.filter_by(recipientID=recipient.id).first()
        print(f"Retrieved Message: {message}") # Success
        assert message is not None, "Message was not stored in database" # Assertions
        assert message.content == "This is a test message.", "Message content not matched" # Check against my input test 
