from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from db import db
from models.users import User
from persistence.datamanager import DataManager
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            access_token = create_access_token(
                identity={'username': email, 'role': user.is_admin})
            return jsonify(access_token=access_token)
    return jsonify({"error": "Invalid credentials"}), 401
