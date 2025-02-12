from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import JWT_SECRET_KEY
from routes.auth import auth_bp  # Import the auth routes
from models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY  # Set JWT secret key

db.init_app(app)
jwt = JWTManager(app)  # Initialize JWT extension

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

