from flask import Blueprint, jsonify, request
from persistence.datamanager import DataManager
from validate_email_address import validate_email
import json
import datetime
import os

user_api = Blueprint("user_api", __name__)
datamanager = DataManager(flag=1)


@user_api.route("/users", methods=["POST", 'GET'])
def add_user():
    """
    Function used to create a new user, send it to the database datamanager
    and read a list of existing users.
    """
    from models.users import User
    if request.method == "POST":
        user_data = request.get_json()
        if not user_data:
            return jsonify({"Error": "Problem during user creation."}), 400

        email = user_data.get("email")
        first_name = user_data.get("first_name")
        last_name = user_data.get("last_name")

        if not all([email, first_name, last_name]):
            return jsonify({"Error": "Missing required field."}), 400
        if not all(c.isascii()
                   for c in first_name) or not first_name.isalpha():
            return jsonify(
                {"Error": "First name must contain only ascii characters."}), 400
        if not all(c.isascii() for c in last_name) or not first_name.isalpha():
            return jsonify(
                {"Error": "Last name must contain only ascii characters."}), 400

        is_email_valid = validate_email(email)
        if not is_email_valid:
            return jsonify({"Error": "Email not valid"}), 400
        try:

            with open("/home/hbnb/hbnb_data/User.json", 'r') as f:

                if user_data["email"] in f.read():
                    return jsonify({"Error": "User already exists"}), 409
        except FileNotFoundError:
            pass

        new_user = User(email, first_name, last_name)
        if not new_user:
            return jsonify({"Error": "setting up new user"}), 500
        else:
            datamanager.save(new_user.to_dict())
            return jsonify({"Success": "User added"}), 201

    else:
        try:

            with open("/home/hbnb/hbnb_data/User.json", 'r', encoding='utf-8') as f:

                users = json.load(f)
                return jsonify(users), 200
        except FileNotFoundError:
            return jsonify({"Error": "No user found"}), 404


@user_api.route("/users/<string:id>", methods=['GET', 'DELETE', 'PUT'])
def get_user(id):
    """
    Function used to read, update or delete a specific user's info
    from the database
    """
    if request.method == 'GET':
        users = datamanager.get("User", id)
        if not users:
            return jsonify({"Error": "User not found"}), 404
        return jsonify(users), 200

    if request.method == 'DELETE':
        users = datamanager.get("User", id)
        if not users:
            return jsonify({"Error": "User not found"}), 404
        users = datamanager.delete("User", id)
        if not users:
            return jsonify({"Success": "User deleted"}), 200

    if request.method == 'PUT':
        user_data = request.get_json()
        user = datamanager.get("User", id)
        if not user:
            return jsonify({"Error": "User not found"}), 404
        user["email"] = user_data["email"]
        user["first_name"] = user_data["first_name"]
        user["last_name"] = user_data["last_name"]
        try:
            with open("data/User.json", 'r') as f:
                if user_data["email"] in f.read():
                    return jsonify({"Error": "User already exists"}), 409
        except FileNotFoundError:
            pass
        datamanager.update(user, id)
        return jsonify({"Success": "User updated"}, user), 200
