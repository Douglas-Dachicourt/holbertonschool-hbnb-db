from flask import Blueprint, jsonify, request
from models.country import Country
from persistence.datamanager import DataManager
import json
import pycountry
country_api = Blueprint("country_api", __name__)


@country_api.route("/countries", methods=["POST", 'GET'])
def country():
    """
    Function used to create a new country, send it to the database datamanager
    """
    list_countries = []
    for country in pycountry.countries:
        list_countries.append(Country(country.name, country.alpha_2).to_dict())
    return jsonify(list_countries), 200


@country_api.route("/countries/<country_code>", methods=["GET"])
def get_country(country_code):
    """
    Function used to retrieve details of a specific country by its code
    """
    country = pycountry.countries.get(alpha_2=country_code.upper())
    if country:
        country_details = Country(country.name, country.alpha_2).to_dict()
        return jsonify(country_details), 200
    else:
        return jsonify({"error": "City not found"}), 404


@country_api.route("/countries/<country_code>/cities", methods=["GET"])
def get_country_cities(country_code):
    """
    Function used to retrieve all cities belonging to a specific country
    """
    # Retrieve the country object using the country code
    country = pycountry.countries.get(alpha_2=country_code.upper())
    if country:
        # Get the list of cities for the country
        cities = get_cities_by_country(country)
        if cities:
            return jsonify(cities), 200
        else:
            return jsonify({"error": "Cities not found"}), 404
    else:
        return jsonify({"error": "Country not found"}), 404


def get_cities_by_country(country):
    """
    Helper function to retrieve all cities belonging to a specific country
    """
    # Implement logic to retrieve cities for the country need to find api for
    # that
    with open('/home/hbnb/hbnb_data/cities.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for city in data:
            if city.get('id') == country.alpha_2.lower():

                return city['city']
