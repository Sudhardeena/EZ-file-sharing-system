# EZ-file-sharing-system
A simple file-sharing system built with Flask, SQLite, and JWT-based authentication.
app deployed at : https://ez-file-sharing-system.onrender.com

Requirements
Python 3.x
Flask
Flask-SQLAlchemy
Flask-JWT-Extended
Flask-Bcrypt
Flask-Migrate
Setup Instructions
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/EZ-file-sharing-system.git
cd EZ-file-sharing-system
Create a virtual environment and activate it:

bash
Copy code
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Create a .env file in the root of the project and add the following configuration:

env
Copy code
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///database.db
Initialize the database:

bash
Copy code
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
Run the Flask application:

bash
Copy code
python app.py
API Endpoints
1. Register User
URL: /register

Method: POST

Description: Registers a new user. The user provides a username, email, and password. The password is hashed using bcrypt.

Request Body (JSON):

json
Copy code
{
  "username": "john_doe",
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
Response (Success):

json
Copy code
{
  "message": "User registered successfully!"
}
Response (Error - Missing fields):

json
Copy code
{
  "message": "Missing required fields!"
}
Response (Error - Email already registered):

json
Copy code
{
  "message": "Email already registered!"
}
2. Login and Get JWT Token
URL: /login

Method: POST

Description: Logs in a user by verifying their email and password. If successful, a JWT token is returned to authenticate future requests.

Request Body (JSON):

json
Copy code
{
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
Response (Success):

json
Copy code
{
  "message": "Login successful!",
  "access_token": "<JWT_TOKEN>"
}
Response (Error - Missing fields):

json
Copy code
{
  "message": "Missing email or password!"
}
Response (Error - Invalid credentials):

json
Copy code
{
  "message": "Invalid password!"
}
Response (Error - User not found):

json
Copy code
{
  "message": "User not found!"
}
Running the Application
To run the application locally, follow the setup steps above and then run:

bash
Copy code
python app.py
The app will be accessible at http://127.0.0.1:5000.



Future Enhancements
Implement file upload functionality for ops users only.
Allow users to download files they uploaded.
Add email confirmation functionality.
Improve error handling and validation.
