from flask import Blueprint, request, jsonify, current_app
from app import db, bcrypt
from models import User
from flask_jwt_extended import create_access_token

# Define the blueprint for routes
main = Blueprint('main', __name__)

@main.route('/')
def welcome():
    return '<h1>Welcome Everyone</h1>'

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate input
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Missing required fields!"}), 400

    # Check if the email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already registered!"}), 400

    # Hash the password using bcrypt
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Create the new user
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        is_ops_user=data.get('is_ops_user', False),  # Optional field in the request body
        is_email_confirmed=data.get('is_email_confirmed', False)  # Optional field in the request body
    )

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate input
    if not data.get('email') or not data.get('password'):
        return jsonify({"message": "Missing email or password!"}), 400

    # Check if the user exists in the database
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({"message": "User not found!"}), 404

    # Verify the password using bcrypt
    if not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid password!"}), 401

    # Generate JWT token
    access_token = create_access_token(identity=user.id)

    return jsonify({"message": "Login successful!", "access_token": access_token}), 200
