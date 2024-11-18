from flask import Blueprint, request, jsonify, current_app

from flask_jwt_extended import create_access_token,  jwt_required, get_jwt_identity

# Define the blueprint for routes
main = Blueprint('main', __name__)

@main.route('/')
def welcome():
    return '<h1>Welcome Everyone</h1>'

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    from app import db, bcrypt
    from models import User

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

    from models import User
    from app import db, bcrypt

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


ALLOWED_EXTENSIONS = {'pptx', 'docx', 'xlsx'}

def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/upload', methods=['POST'])
@jwt_required()  # Ensure the user is logged in
def upload_file():
    current_user_id = get_jwt_identity()  # Get the current logged-in user

    from models import User

    user = User.query.get(current_user_id)

    # Check if the current user is an ops_user
    if not user or not user.is_ops_user:
        return jsonify({"message": "Only ops users can upload files!"}), 403

    if 'file' not in request.files:
        return jsonify({"message": "No file part!"}), 400

    file = request.files['file']

    # Check if the file has a valid extension
    if file and allowed_files(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "File uploaded successfully!"}), 201
    else:
        return jsonify({"message": "Invalid file type!"}), 400