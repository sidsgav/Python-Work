# * This is Gavin's Code  - Additions from team members are made in their own branch but extended from mine *

# Import the required modules for functionality
import random
from flask import Flask, render_template, request, redirect, session, url_for, flash, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import re # Import regex here for input validation
from datetime import datetime, timezone

# Initialise the 'Flask' app
app = Flask(__name__)

# Database configuration - reference to 'sqlitestudio' - basic for first sprint
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///komodo_hub.db' # SQLite database path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey' # Secret key for session security
db = SQLAlchemy(app) # Initialise SQLAlchemy

# Initialise Flask login correctly
login_manager = LoginManager() # 'LoginManager' instance from imported libraries 
login_manager.init_app(app) # Attach LoginManager to 'Flask' app
login_manager.login_view = 'login' # Set the default login view

# Define the school model which manages profiles linked to schools and specific access codes
class School(db.Model):

    __tablename__ = "schools"  # Explicit table name
    id = db.Column(db.Integer, primary_key=True) # Auto-incremented school ID (PK)
    name = db.Column(db.String(100), unique=True, nullable=False) # The students name
    library = db.Column(db.Text, nullable=True) # The schools total contributions made, added to library here
    accessCode = db.Column(db.String(50), unique=True, nullable=False) # Secure access code for students

# Message model for teacher and student communication - between themselves
class Message(db.Model):

    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    senderID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Sender of message
    recipientID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Who receives it
    content = db.Column(db.Text, nullable=False) # What is actually in the message - could be file/ writing [etc]
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))    
    readStatus = db.Column(db.Boolean, default=False) # Whether the recipient has unread/ read [...]

    sender = db.relationship('User', foreign_keys=[senderID], backref='sent_messages')  # Defining relationships between for easier access in db
    recipient = db.relationship('User', foreign_keys=[recipientID], backref='received_messages')

    def __repr__(self):
        return f"<Message from {self.senderID} to {self.recipientID} at {self.timestamp}>"


# Define the user model before using it - *some changes have been made here*
class User(db.Model, UserMixin):

    __tablename__ = "users"  # Explicit table name
    id = db.Column(db.Integer, primary_key=True) # Auto-incremented user ID for (PK) storage
    username = db.Column(db.String(80), unique=True, nullable=False) # Unique username so not same as others for sign-up
    password = db.Column(db.String(255), nullable=False) # Hashed password storage for utmost security esepcially for student protection
    accountType = db.Column(db.String(20), nullable=False, default='student') # User account type: (student, teacher, public user)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=True) # Link students to a school and nullable True as different account types possible
    profileCustomisation = db.Column(db.Text, nullable=True) # Store avatars, themes, and other settings for requirment met

    def __repr__(self):
        return f"<User {self.username}, Account Type: {self.accountType}>" 

School.students = db.relationship('User', backref='school', lazy=True)

# Define Conservation Challenge model
class ConservationChallenge(db.Model):
    __tablename__ = "conservation_challenges"
    id = db.Column(db.Integer, primary_key=True) # Primary key
    titleOfChallenge = db.Column(db.String(100), nullable=False) # The title of the challenge
    descOfChallenge = db.Column(db.Text, nullable=False) # Description of the challenge 
    noOfPoints = db.Column(db.Integer, nullable=False, default = 5) # The number of points awarded per challenge success - with def being 5

# Define the User's Contribution model
class Contribution(db.Model):
    __tablename__ = "contributions"
    id = db.Column(db.Integer, primary_key=True) # primary key for database relation here
    userID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User
    challengeID = db.Column(db.Integer, db.ForeignKey('conservation_challenges.id'), nullable=False)  # Foreign key to Challenge
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())  # Timestamp of when hey submitted it

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

print("Flask-Login success!.") # Print debug message to confirm flask-login initialisation(debug mode test)

def is_valid_username(username): # Input validation function so random input not allowed

    """Validate username: Only allows alphanumeric characters and underscores, 3-20 characters long.""" # One security measure so prevents easy brute-force attack
    return re.match(r"^[a-zA-Z0-9_]{3,20}$", username) # Input validation

@app.route('/register', methods=['GET', 'POST']) # Secure Route - register a new user 
def register():

    if request.method == 'POST':
        username = request.form['username'].strip() # Gets rid of trailing spaces
        password = request.form['password'].strip() # Gets rid of trailing spaces
        accountType = request.form.get('accountType', 'student') # Gets the user account type, defaulting to 'student'
        try:
            school_id = int(request.form.get('school_id', 0)) if request.form.get('school_id') else None
        except ValueError:
            school_id = None  # If invalid, set to None
        if not is_valid_username(username): # Validate username format for input val
            flash(" You have entered an invalid username. The minimum is 8 characters and please use a combination of characters.", "danger")
            return redirect(url_for('register'))
        existing_user = User.query.filter_by(username=username).first() # Ensure the use of a unique username
        if existing_user:
            flash(" This username is already in use, please try another.", "danger") # Appropiate message display
            return redirect(url_for('register'))  
        if len(password) < 8 or not re.search(r"\d", password) or not re.search(r"[A-Z]", password): # Validate password strength using 'regex' again
            flash(" Password must be at least 8 characters long, include a number and an uppercase letter please.", "warning")  
            return redirect(url_for('register'))
        hashedPassword = generate_password_hash(password, method='pbkdf2:sha256')  # Hash the password before storing it in the database
        # Create new user entry in the database with associated account type
        new_user = User(username = username, password = hashedPassword, accountType = accountType, school_id = school_id)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration success! You can now log in.", "success")  
        return redirect(url_for('login'))  
    return render_template('register.html')  

# Secure route - login the user if only registration first
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        accountType = request.form.get('accountType')
        if not is_valid_username(username): # Validate username format before querying the database
            flash(" Invalid username format.", "danger")
            return redirect(url_for('login'))
        user = User.query.filter_by(username = username, accountType = accountType).first()  # Ensures the account type matches
        if user and check_password_hash(user.password, password): # Check user existence and verify hashed password ^
            login_user(user)  
            flash(" Login successful.", "success")  
            return redirect(url_for('dashboard'))  
        else:
            flash(" Invalid username or password, please try again.", "danger") # Appropiate message display using flash for response
    return render_template('login.html')  

# Secure route - user dashboard - could me modified to change for redirection
@app.route('/dashboard')
@login_required  
def dashboard():

    if current_user.accountType == "student":
        return render_template('student_dash.html', user=current_user) # what displayed to student/ accessible
    elif current_user.accountType == "teacher":
        return render_template('teacher_dash.html', user=current_user) # what to be accessed by teachers who use it
    elif current_user.accountType == "public":
        return render_template('public_dash.html', user=current_user) # what to be accessed by public users and their restrictions
    else:
        return abort(403) # Unauthorised access dependent on access type

# Secure Route - Logout
@app.route('/logout') # Allows user to logout once logged in/ signed in
@login_required
def logout():

    logout_user()  
    flash("Logout Successful.", "info") # Appropiate message banner style
    return redirect(url_for('login'))  

# Account type-based access control decorator
def account_type_required(required_type):  

    """Restrict access based on user account type for different capabailites - access."""

    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.accountType != required_type: # Not correct account type access**
                abort(403)  # Forbidden access as user lacks required account type
            return f(*args, **kwargs)
        return wrapped_function
    return decorator

# Route to display the messaging dashboard which shows all messages related to the current user and dependent on their acc type
@app.route('/messages')
@login_required # Ensure only authenticated users can access this page - featire available to certain users remember!
def messages():
    userMessages = Message.query.filter( # Retreive user messages for that sepcific user fromm= the db
        (Message.senderID == current_user.id) | (Message.recipientID == current_user.id)
    ).order_by(Message.timestamp.desc()).all() # Latest one
    all_users = User.query.filter(
        User.id != current_user.id,
        User.accountType.in_(["student", "teacher"]) # Include only these account types in this route for account tyoe due to security - no general users allowed due to student protection
    ).all()
    return render_template('messages.html', # render corresponding template 
                           messages=userMessages, 
                           all_users=all_users)

# Route to send a new message
@app.route('/messages/send', methods=['POST'])
@login_required # User must be logged in before they are eligible to perform this
def send_message():

    recipientID = request.form.get('recipientID') # Retrieve the 'recipientID' from form and it should correspond to a valid user in the system that is logged in
    content = request.form.get('content').strip() # Remove any leading/trailing whitespace
    print(f"➡️ Incoming Message Data: recipientID={recipientID}, content={content}")
    if not recipientID or not content: # These are used to validate input - make sure not empty/ NULL
        flash("Recipient and content are required.", "danger") # If it proves to be empty, it shows a flash message to the user indicating the error
        return redirect(url_for('messages')) # Redirect the user back to the messaging dashboard
    
    recipient_user = db.session.get(User, recipientID)
    if (not recipient_user or 
        recipient_user.id == current_user.id or 
        recipient_user.accountType == "public"): # Make absoloute sure on account type message account restrictions
        flash("Invalid recipient. You can only message students or teachers.", "danger")
        return redirect(url_for('messages'))
    
    new_message = Message(senderID=current_user.id, recipientID=recipientID, content=content) # Security check to ensure confidentiality and protection - verify that the sender is a teacher and the recipient is an enrolled student [*mod*]
    db.session.add(new_message) # Add the new message to the database and add it
    print(f"Message saved: {new_message}")
    db.session.commit()
    flash("Message sent successfully!", "success") # This is a flash message which indicates the message was sent successfully
    return redirect(url_for('messages')) # *Redirect*

# Route to mark a message as read - endpoint via an AJAX POST request
@app.route('/messages/<int:message_id>/read', methods=['POST'])
@login_required 
def mark_message_read(message_id):

    message = Message.query.get_or_404(message_id) # If msg does not exist when retreiving message object - '404 error' returned 
    if message.recipientID != current_user.id: # Security check to ensure confidentiality and security - only the recipient of the message can mark it as read
        abort(403) # Unauthorised access error return
    message.readStatus = True # Update 'readStatus' var when msg read
    db.session.commit() # Update database
    return jsonify({"status": "success"}) # A JSON response used in the UI which shows success message

# Route which returns number of unread messages for current user
@app.route('/messages/notifications')
@login_required 
def message_notifications():

    unread_count = Message.query.filter_by(recipientID=current_user.id, readStatus=False).count() # Where 'readStatus' var is set to False and count number to calculate
    return jsonify({"unread_count": unread_count}) # Returns unread total count as a JSON response for UI output

# Secure Route - homepage - initial view
@app.route('/')
def home():

    return render_template('home.html')  # Render the homepage for user

@app.route('/student/dashboard') # Requires future attention
@login_required
@account_type_required('student')  
def student_dashboard():

    """Displays the student's dashboard with customisation options."""
    return render_template('student_dash.html', user=current_user)

# Secure route - teacher dash needs future dev
@app.route('/teacher/dashboard')
@login_required
@account_type_required('teacher')  
def teacher_dashboard():

    """Displays the teacher's dashboard with student management options and other stuff[...."""
    students = User.query.filter_by(accountType='student').all()
    return render_template('teacher_dash.html', user=current_user, students=students)

@app.route('/public/dashboard')
@login_required
@account_type_required('public')  
def public_dashboard():

    """Displays the public user dashboard with conservation programs."""
    return render_template('public_dash.html', user=current_user)

# Route to access Learning Materials
@app.route('/learning_materials')
@login_required  # Ensures only authenticated users can access this route
def learning_materials():
    """
    This route renders the Learning Materials page.
    Optionally, you can add further role-based checks if only certain users should access this.
    """
    return render_template('learning_materials.html')  # Render the corresponding template

# Route to view Student Progress Report
@app.route('/student_progress_report')
@login_required  # User must be logged in
def student_progress_report():
    """
    This route renders the Student Progress Report page.
    It displays a detailed report of student progress.
    """
    return render_template('student_progress_report.html')  # Render the corresponding template

# Route to report a wildlife sighting
@app.route('/report_sighting')
@login_required  # Only logged-in users can report sightings
def report_sighting():
    """
    This route renders the Report a Sighting page.
    Users can submit details of wildlife sightings through this interface.
    """
    return render_template('report_sighting.html')  # Render the corresponding template

# Route to access Interactive Games
@app.route('/interactive_games')
@login_required  # User must be authenticated
def interactive_games():
    """
    This route renders the Interactive Games page.
    It provides conservation-themed games and quizzes for engagement.
    """
    return render_template('interactive_games.html')  # Render the corresponding template

# Route for Secure Student Access
@app.route('/secure_student_access')
@login_required # Ensures only authenticated users can access this route
def secure_student_access(): # This route renders the student security route page where each teacher can generate unique access codes here for their students

    return render_template('secure_student_access.html')  # Render the corresponding template

# Secure Route - test for flask - (remove later)
@app.route('/test')
def test():

    return "<h1>Flask is running correctly!</h1>"

# Prevent Clickjacking (Security Headers)
@app.after_request
def add_security_headers(response):

    """Adds security headers to HTTP responses."""
    response.headers["X-Frame-Options"] = "DENY" # Prevents clickjacking attacks
    response.headers["X-Content-Type-Options"] = "nosniff" # Prevents MIME type sniffing
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self'; img-src 'self'"# Restricts external content
    # (More risk but not industry level project so it's okay - ()'unsafe-inline';))
    return response

# Secure route to view all the available challenges user can choose
@app.route('/challenges')
def view_challenges():
    challenges = ConservationChallenge.query.all() # Retreive all the available challenges
    return render_template('challenges.html', challenges = challenges) # Render the corresponding challenges template

# Route to submit a conservation contribution
@app.route('/submit_contribution/<int:challengeID>', methods=['POST'])
@login_required # This ensures only logged in users can contribute - (should be for public users mainly but can opt for others too)
def submit_contribution(challengeID):
    existingContribution = Contribution.query.filter_by(user_id = current_user.id, 
                                                        challengeID = challengeID).first()
    if existingContribution: # If already contributed before
        flash("You have already participated in this challenge.", "warning") # Provide appropiate flash message
        return redirect(url_for('view_challenges'))
    
    newContribution = Contribution(userId = current_user.id, 
                                   challengeID = challengeID)
    db.session.add(newContribution) # Add the new contribution to the database
    db.session.commit()
    flash("Contribution submitted successfully.", "success") # Appropiate flash message for this here
    return redirect(url_for('view_challenges')) # Return appropiate redirect for this

# secure route to display the sleaderboard
@app.route('/leaderboard')
def view_leaderboard():
    leaderboardData = db.session.query(User.username, 
                                       db.func.count(Contribution.id).label("totalContributions"))
    leaderboardData = leaderboardData.join(Contribution).group_by(User.id).order_by(db.desc("totalContributions")).all() # (Join)
    return render_template('leaderboard.html', leaderboard=leaderboardData) # Render the respective leaderboard page

# Kuba's redirect code here:

# Word scramble game secure route
@app.route("/scramble", methods=["GET", "POST"])
def scramble_game():
    if "original_word" not in session:
        words = ['java', 'rhinoceros', 'deforestation', 'conservation', 'komodo']
        session["original_word"] = random.choice(words)
        session["scrambled_word"] = "".join(random.sample(session["original_word"], len(session["original_word"])))
        session["message"] = ""

    if request.method == "POST":
        guess = request.form.get("guess", "").lower()
        if guess == session["original_word"]:
            session["message"] = "Correct! "
        else:
            session["message"] = "Try again "
    
    return render_template("scramble.html", scrambled_word=session["scrambled_word"], message=session["message"])

@app.route("/restart_scramble")
def restart_scramble():
    session.clear()
    return redirect(url_for("scramble_game"))

# Quiz Game Route
@app.route("/quiz", methods=["GET", "POST"])
def quiz_game():
    questions = [
        {"question": "Which endangered species is found in Indonesia?", "options": ["Javan Rhino", "Tiger", "Penguin", "Elephant"], "answer": "Javan Rhino"}
    ]

    if request.method == "POST":
        score = sum(request.form.get(f'question-{i}') == q["answer"] for i, q in enumerate(questions))
        return render_template("quiz_result.html", score=score, total=len(questions))
    
    return render_template("quiz.html", questions=questions)

@app.route("/restart_quiz")
def restart_quiz():
    return redirect(url_for("quiz_game"))

# Hangman game route
@app.route("/hangman", methods=["GET", "POST"])
def hangman_game():
    return render_template("hangman.html")


# Run Flask
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Ensures database & tables exist
    app.run(debug=True)
