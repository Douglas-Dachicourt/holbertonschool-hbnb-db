from flask import Blueprint, jsonify, request
from persistence.datamanager import DataManager
from validate_email_address import validate_email
from uuid import UUID

# from flask_jwt_extended import {
# jwt_required, create_access_token, get_jwt_identity}
import json
import datetime
import os

user_api = Blueprint("user_api", __name__)
datamanager = DataManager(flag=1)


@user_api.route("/users", methods=["POST", "GET"])
def add_or_list_users():
    """
    Add a new user or list all existing users.

    POST method:
    Creates a new user with provided JSON data containing 'email',
    'first_name', 'last_name', and 'password'.
    Validates email format and checks for existing users before adding.
    Returns a success message if user is added successfully, or an error
    message if failed.

    GET method:
    Retrieves a list of all users from the database.
    Returns a JSON array of user objects containing 'id', 'email',
    'first_name', and 'last_name'.

    Returns:
        JSON: Response message with appropriate HTTP status code.
    """

    from models.users import User

    if request.method == "POST":
        user_data = request.get_json()

        if not user_data:
            return jsonify({"error": "No data provided"}), 400

        email = user_data.get("email")
        first_name = user_data.get("first_name")
        last_name = user_data.get("last_name")
        password = user_data.get("password")

        if not all([email, first_name, last_name]):
            return jsonify({"error": "Missing required field"}), 400

        is_email_valid = validate_email(email)
        if not is_email_valid:
            return jsonify({"error": "Email not valid"}), 400

        # Check if user already exists in the database
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "User already exists"}), 409

        # Create a new User object
        new_user = User(email=email, first_name=first_name,
                        last_name=last_name, password=password)

        try:
            # save the user to the database
            datamanager.save_to_database(new_user)
            return jsonify({"message": "User added successfully"}), 201
        except Exception as e:
            return jsonify({"error": f"Failed to add user: {str(e)}"}), 500

    elif request.method == "GET":
        users = User.query.all()
        user_list = []
        for user in users:
            user_list.append({
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            })
        return jsonify(user_list), 200


@user_api.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"])
def get_update_delete_user(user_id):
    """
    Retrieve, update, or delete a specific user by user ID.

    GET method:
    Retrieves the details of a user identified by 'user_id'.
    Returns a JSON object with 'id', 'email', 'first_name', and
    'last_name'.
    Returns an error message if the user is not found.

    PUT method:
    Updates the details of an existing user identified by 'user_id' with
    provided JSON data.
    Returns a success message if user is updated successfully, or an error
    message if failed.

    DELETE method:
    Deletes an existing user identified by 'user_id'.
    Returns a success message upon successful deletion.

    Args:
        user_id (str): The unique identifier of the user.

    Returns:
        JSON: Response message with appropriate HTTP status code.
    """
    from models.users import User

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == "GET":
        return jsonify({
            "id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }), 200

    elif request.method == "PUT":
        user_data = request.get_json()

        user.email = user_data.get("email", user.email)
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)

        try:
            # Update the user through datamanager
            datamanager.update_database(User, user_id, user_data)
            return jsonify({"message": "User updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to update user: {str(e)}"}), 500

    elif request.method == "DELETE":
        # Deletion via DataManager
        datamanager.delete_from_database(User, user_id)
        return jsonify({"message": "User deleted successfully"})
