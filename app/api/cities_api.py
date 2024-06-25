from flask import Blueprint, jsonify, request
from models.city import City
from persistence.datamanager import DataManager
import json
import datetime
import os
datamanager = DataManager(flag=5)
cities_api = Blueprint("cities_api", __name__)


@cities_api.route("/cities", methods=["POST", 'GET'])
def cities():
    """
    Function used to create a new city, send it to the database datamanager
    """
    if request.method == "POST":
        city_data = request.get_json()
        city_id = city_data.get('id')
        city_name = city_data.get('name')

        if not city_id or not city_name:
            return jsonify({"Error": "Invalid data"}), 400

        new_city = City(city_name, city_id).to_dict()

        file_path = '/home/hbnb/hbnb_data/cities.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        with open(file_path, 'r+', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

            for entry in data:
                if entry.get('id') == city_id:
                    # Check if the city already exists
                    if any(
                            city['name'] == city_name for city in entry['city']):
                        return jsonify({"Error": "City already exists"}), 400

                    entry['city'].append(new_city)

                    f.seek(0)
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    f.truncate()

                    return jsonify({"Success": "City added"}), 201

            return jsonify({"Error": "Country ID not found"}), 404

    if request.method == "GET":
        with open('/home/hbnb/hbnb_data/cities.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return jsonify(data), 200


@cities_api.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
def get_city(city_id):
    """
    Function used to read, update or delete a specific city's info
    from the database
    """
    if request.method == "GET":
        with open('/home/hbnb/hbnb_data/cities.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for entry in data:
                for city in entry["city"]:
                    if city.get('uniq_id') == city_id:
                        return jsonify(city), 200
            return jsonify({"Error": "City not found"}), 404
    if request.method == "PUT":
        city_data = request.get_json()
        with open('/home/hbnb/hbnb_data/cities.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for entry in data:
                for city in entry["city"]:
                    if city.get('uniq_id') == city_id:
                        city['name'] = city_data.get('name')
                        city["updated_at"] = datetime.datetime.now().isoformat()
                        with open('/home/hbnb/hbnb_data/cities.json', 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)
                        return jsonify({"Success": "City updated"}, city), 200
    if request.method == "DELETE":
        with open('/home/hbnb/hbnb_data/cities.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for entry in data:
                for city in entry["city"]:
                    if city.get('uniq_id') == city_id:
                        entry["city"].remove(city)
                        with open('/home/hbnb/hbnb_data/cities.json', 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)
                        return jsonify({"Success": "City deleted"}), 200
            return jsonify({"Error": "City not found"}), 404
