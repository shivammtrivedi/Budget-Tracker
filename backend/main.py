from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from config import JWT_SECRET_KEY, app, db  # Import app & db from config
from routes.auth import auth_bp  # Import authentication routes
from models import User, Transaction  # Import models

# Initialize JWT authentication
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")

ADMIN_EMAIL = "shivammtrivedi@gmail.com"

@app.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    # Allow only if my email
    if not current_user or current_user.email != ADMIN_EMAIL:
        return jsonify({"error": "Unauthorized"}), 403

    users = User.query.all()
    json_users = [user.to_json() for user in users]
    return jsonify({"users": json_users})

@app.route("/transactions", methods=["GET"])
def get_transactions():
    transactions = Transaction.query.all()
    json_transactions = [t.to_json() for t in transactions]  # Convert transactions to JSON
    return jsonify({"transactions": json_transactions})

# Run app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create tables

    app.run(debug=True, port=5001)
