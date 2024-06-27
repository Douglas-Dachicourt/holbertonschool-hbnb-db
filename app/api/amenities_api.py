from flask import Blueprint, jsonify, request
from models.amenity import Amenity
from persistence.datamanager import DataManager
import json
amenities_api = Blueprint("amenities_api", __name__)
datamanager = DataManager(flag=3)


@amenities_api.route("/amenities", methods=["POST", 'GET'])
def add_amenity():
    """
    Function used to create a new amenity, send it to the database datamanager
    and read a list of existing amenities.
    """
    if request.method == "POST":
        amenity_data = request.get_json()
        if not amenity_data:
            return jsonify({"Error": "Problem during amenity creation."}), 400

        name = amenity_data.get("name")
        if not name:
            return jsonify({"Error": "Missing required field."}), 400

        new_amenity = Amenity(name)
        if not new_amenity:
            return jsonify({"Error": "setting up new amenity"}), 500
        else:
            existing_amenities = Amenity.query.filter_by(name=name).first()
            if existing_amenities:
                return jsonify({"Error": "Amenity already exists"}), 409

            new_amenity = Amenity(name=name)

            datamanager.save_to_database(new_amenity)
            return jsonify({"Success": "Amenity added"}), 201
    else:
        try:
            amenities = Amenity.query.all()
            amenity_list = []
            for amenity in amenities:
                amenity_list.append({
                    "id": amenity.id,
                    "name": amenity.name
                })
            return jsonify(amenity_list), 200
        except Exception as e:
            return jsonify({"Error": "No amenity found"}), 404


@amenities_api.route("/amenities/<string:id>",
                    methods=['GET', 'DELETE', 'PUT'])
def get_amenity(id):
    """
    Function used to read, update or delete a specific amenity's info
    from the database
    """
    amenities = Amenity.query.filter_by(id=id).first()
    if request.method == "GET":
        if amenities:
            return jsonify({"id": str(amenities.id),
            "name": amenities.name}), 200
        if not amenities:
            return jsonify({"Error": "Amenity not found"}), 404

    if request.method == "DELETE":
        if datamanager.delete_from_database(Amenity, id):
            return jsonify({"Success": "Amenity deleted"}), 200
        else:
            return jsonify({"Error": "Amenity not found"}), 404


    if request.method == "PUT":
        if not amenities:
            return jsonify({"Error": "Amenity not found"}), 404
        amenity_data = request.get_json()
        amenities.name = amenity_data.get("name", amenities.name)
        try:
            datamanager.update_database(Amenity, id, amenity_data)
            return jsonify({"Success": "Amenity updated"}), 200
        except Exception as e:
            return jsonify({"Error": "An error occurred"}), 500