from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Ensure SECRET_KEY and JWT_SECRET_KEY are set
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # Change this!
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)  # Use SECRET_KEY as fallback

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY  # Ensures JWT works

db = SQLAlchemy(app)
