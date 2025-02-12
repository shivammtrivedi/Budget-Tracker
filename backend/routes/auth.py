from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from models import db, User
from utils.security import hash_password, verify_password
from datetime import timedelta
import re

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsIml \
# hdCI6MTczOTM0NjY1NSwianRpIjoiM2JmYmEzMzQtNzcwZC00NzQ3LWE0ND \
# ktZDc0ZTQ0MGE2MjI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIj \
# oxNzM5MzQ2NjU1LCJjc3JmIjoiM2I1OTk5N2ItMzVmZi00NjhiLWIyMjItYTd \
# mNjc2YzQ2ZTBhIiwiZXhwIjoxNzM5MzUwMjU1fQ.fPW6PyGwhWMHRweRgdf60K \
# 6UQuGTb6aDueh0F5OUh7w

auth_bp = Blueprint("auth", __name__)

# User Registration Route
def is_valid_password(password):
    """Check if the password meets the security requirements."""
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must contain at least one special character."
    return None  # No issues, password is valid

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    # Validate password
    password_error = is_valid_password(password)
    if password_error:
        return jsonify({"error": password_error}), 400

    # Hash password and create new user
    new_user = User(email=email, password_hash=hash_password(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# User Login Route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not verify_password(data["password"], user.password_hash):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate JWT token valid for 1 hour
    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))

    return jsonify({"access_token": access_token, "user_id": user.id}), 200

# Protected Route Example (Requires Valid JWT)
@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify({"message": "You have access to this protected route!"}), 200

