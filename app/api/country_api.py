from flask import Blueprint, jsonify, request
from models.country import Country
from models.city import City
from persistence.datamanager import DataManager
import json
import pycountry
from db import db

country_api = Blueprint("country_api", __name__)


@country_api.route("/countries", methods=["POST"])
def add_country():
    """
    Function used to create a new country, send it to the database datamanager
    """
    try:
        for country in pycountry.countries:
            new_country = Country(name=country.name, code=country.alpha_2)
            db.session.add(new_country)
        db.session.commit()
        return jsonify({"message": "Countries added successfully"}), 201
    except Exception as e:
        db.session.rollback()  # Rollback changes if an error occurs
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()  # Ensure session is properly closed

@country_api.route("/countries", methods=["GET"])
def get_countries():
    """
    Retrieves all countries from the database
    """
    countries = Country.query.all()
    country_list = [country.to_dict() for country in countries]
    return jsonify(country_list), 200


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
        return jsonify({"error": "Country not found"}), 404

@country_api.route("/countries/<country_code>/cities", methods=["POST"])
def add_city_to_country(country_code):
    """
    Function to add a city to a specific country
    """
    country = Country.query.filter_by(code=country_code.upper()).first()
    if not country:
        return jsonify({"error": "Country not found"}), 404

    data = request.get_json()
    city_name = data.get('name')

    if not city_name:
        return jsonify({"error": "City name is required"}), 400

    new_city = City(name=city_name, country_id=country.id)
    db.session.add(new_city)
    db.session.commit()
    
    return jsonify(new_city.to_dict()), 201


@country_api.route("/countries/<country_code>/cities", methods=["GET"])
def get_country_cities(country_code):
    """
    Function used to retrieve all cities belonging to a specific country
    """
    country = Country.query.filter_by(code=country_code.upper()).first()
    if country:
        cities = City.query.filter_by(country_id=country.id).all()
        if cities:
            city_list = [city.to_dict() for city in cities]
            return jsonify(city_list), 200
        else:
            return jsonify({"error": "Cities not found"}), 404
    else:
        return jsonify({"error": "Country not found"}), 404
