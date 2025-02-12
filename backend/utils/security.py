from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, decode_token
from datetime import timedelta

# Hash user's password before storing it in DB
def hash_password(password):
    return generate_password_hash(password)

# Verify if provided password matches stored hash
def verify_password(password, hashed_password):
    return check_password_hash(hashed_password, password)

# Generate JWT token for authenticated users
def generate_jwt_token(user_id):
    return create_access_token(identity=user_id, expires_delta=timedelta(hours=1))

# Decode JWT token (for extracting user_id)
def decode_jwt_token(token):
    try:
        decoded_data = decode_token(token)
        return decoded_data["sub"]  # "sub" refers to the user ID stored in the token
    except:
        return None
