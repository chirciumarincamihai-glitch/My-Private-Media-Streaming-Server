from flask import Flask, request, send_file , jsonify
from flask_cors import CORS
import sqlite3
from database import create_user, get_movies,get_user
import os
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

app = Flask(__name__)
CORS(app)
load_dotenv()
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["headers", "query_string"]
app.config["JWT_QUERY_STRING_NAME"] = "token"
jwt = JWTManager(app)


@app.route('/list')
@jwt_required()
def list_movies():
    username = get_jwt_identity()
    user = get_user(username)
    role = user[3]

    movies = get_movies()

    if role == "kid":
        movies = [m for m in movies if m["kid_appropriate"] == 1]

    return jsonify(movies)


@app.route('/<movie>')
@jwt_required()
def home(movie):
    movies = get_movies()
    filename = None
    for m in movies:
        if m['name'] == movie:
            filename = m['filename']
    if filename is None:
        return "Movie not found", 404
    try:
        return send_file(f"../{filename}")
    except:
        return "Error occurred while fetching the movie file", 500


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({"error": "Missing required fields"}), 400

    create_user(username, password, role)
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    token = create_access_token(identity=username)
    if not username or not password:
        return jsonify({"error": "Missing required fields"}), 400

    user = get_user(username)
    if not user or not check_password_hash(user[2], password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful", "token": token}), 200

app.run(host='0.0.0.0')