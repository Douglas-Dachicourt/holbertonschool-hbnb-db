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
    if request.method == "GET":
        amenities = datamanager.get("Amenity", id)
        if not amenities:
            return jsonify({"Error": "Amenity not found"}), 404
        return jsonify(amenities), 200

    if request.method == "DELETE":
        amenities = datamanager.get("Amenities", id)
        if not amenities:
            return jsonify({"Error": "Amenity not found"}), 404
        amenities = datamanager.delete("Amenities", id)
        if not amenities:
            return jsonify({"Success": "Amenity deleted"}), 200

    if request.method == "PUT":
        amenity_data = request.get_json()
        amenity = datamanager.get("Amenity", id)
        if not amenity:
            return jsonify({"Error": "amenity not found"}), 404
        try:
            with open("/home/hbnb/hbnb_data/Amenity.json", 'r', encoding='UTF-8') as f:
                if amenity_data["name"] in f.read():
                    return jsonify({"Error": "Amenity already exists"}), 409
        except FileNotFoundError:
            pass
        amenity["name"] = amenity_data["name"]
        datamanager.update(amenity, id)
        return jsonify({"Success": "Amenity updated"}, amenity), 200
