from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

# Create the Flask app
app = Flask(__name__)

# Load configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Set a secret key for JWT
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')  # SQLite by default
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications to save resources

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
jwt.init_app(app)

# Import and register routes after app initialization to avoid circular imports
from routes import main
app.register_blueprint(main)

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)
