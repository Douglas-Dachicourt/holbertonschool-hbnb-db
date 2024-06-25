from flask import Blueprint, jsonify, request
from models.place import Place
from persistence.datamanager import DataManager
import json
place_api = Blueprint("place_api", __name__)
datamanager = DataManager(flag=2)


@place_api.route("/places", methods=["POST", "GET"])
def add_place():
    """
    Function used to create a new place, send it to the database datamanager
    and read a list of existing places.
    """
    if request.method == "POST":
        place_data = request.get_json()
        if not place_data:
            return jsonify({"Error": "Problem during place creation"})

        name = place_data.get("name")
        description = place_data.get("description")
        address = place_data.get("address")
        latitude = place_data.get("latitude")
        longitude = place_data.get("longitude")
        num_rooms = place_data.get("num_rooms")
        num_bathrooms = place_data.get("num_bathrooms")
        price_per_night = place_data.get("price_per_night")
        max_guests = place_data.get("max_guests")
        # Pas sûr de comment initialiser ces attributs
        # host_id est l'id de la personne qui créé la Place
        # city_id viendra de city_api
        # amenity_ids est l'UUID d'une amenity que l'user veut ajouter
        host_id = place_data.get("host_id")
        amenity_ids = place_data.get("amenity_ids")
        city_id = place_data.get("city_id")

        if not all([name, description, address, latitude, longitude,
                    num_rooms, num_bathrooms, price_per_night, max_guests,
                    city_id, host_id]):
            return jsonify({"Error": "Missing required field."}), 400

        if not (isinstance(arg, str)
                for arg in (name, description, address)):
            raise TypeError({"Error": "TypeError"})
        if not (isinstance(arg, int)
                for arg in (num_bathrooms, num_rooms, max_guests)):
            raise TypeError({"Error": "TypeError"})
        if not (isinstance(arg, (float, int))
                for arg in (latitude, longitude, price_per_night)):
            raise TypeError({"Error": "TypeError"})

        new_place = Place(name, description, address, city_id, latitude,
                          longitude, host_id, num_rooms, num_bathrooms,
                          price_per_night, max_guests, amenity_ids)
        if not new_place:
            return jsonify({"Error": "setting up new place"}), 500
        else:
            if amenity_ids is None:
                datamanager.save(new_place.to_dict())
                return jsonify({"Success": "Place added"},
                               new_place.to_dict()), 201
            else:
                with open("/home/hbnb/hbnb_data/Amenity.json", 'r') as f:
                    amenities = json.load(f)

            # Check if the amenity_id exists in the place_data
                    for amenity in amenities:
                        if amenity.get("uniq_id") == amenity_ids:
                            datamanager.save(new_place.to_dict())
                            return jsonify(
                                {"Success": "Place added"}, new_place.to_dict()), 201
                    return jsonify({"Error": "Amenity not found"}), 409
    else:
        try:
            with open("/home/hbnb/hbnb_data/Place.json", 'r', encoding='UTF-8') as f:
                places = json.load(f)
                return jsonify(places), 200
        except FileNotFoundError:
            return jsonify({"Error": "No place found"}), 404


@place_api.route("/places/<string:id>", methods=["GET", "DELETE", "PUT"])
def get_place(id):
    """
    Function used to read, update or delete a specific place's info
    from the database
    """
    if request.method == "GET":
        places = datamanager.get("Place", id)
        if not places:
            return jsonify({"Error": "Place not found"}), 404
        return jsonify(places), 200

    if request.method == "DELETE":
        places = datamanager.get("Places", id)
        if not places:
            return jsonify({"Error": "Place not found"}), 404
        places = datamanager.delete("Places", id)
        if not places:
            return jsonify({"Success": "Place deleted"}), 200

    if request.method == "PUT":
        place_data = request.get_json()
        place = datamanager.get("Place", id)
        if not place:
            return jsonify({"Error": "User not found"}), 404
        place["name"] = place_data["name"]
        place["description"] = place_data["description"]
        place["address"] = place_data["address"]
        place["latitude"] = place_data["latitude"]
        place["longitude"] = place_data["longitude"]
        place["num_rooms"] = place_data["num_rooms"]
        place["num_bathrooms"] = place_data["num_bathrooms"]
        place["price_per_night"] = place_data["price_per_night"]
        place["max_guests"] = place_data["max_guests"]
        place["host_id"] = place_data["host_id"]
        place["amenity_ids"] = place_data["amenity_ids"]
        place["city_id"] = place_data["city_id"]
        datamanager.update(place, id)
        return jsonify({"Success": "Place updated"}, place), 200
