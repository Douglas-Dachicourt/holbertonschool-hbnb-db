import unittest
from flask import Flask
from flask.testing import FlaskClient
from api.country_api import country_api, get_cities_by_country
from models.country import Country
from persistence.datamanager import DataManager
from unittest.mock import patch, MagicMock
import json

class CountryApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(country_api)
        self.app.testing = True
        self.client = self.app.test_client()
        self.client: FlaskClient

    @patch('api.country_api.pycountry.countries')
    def test_get_countries(self, MockCountries):
        mock_country = MagicMock()
        mock_country.name = "United States"
        mock_country.alpha_2 = "US"
        MockCountries.__iter__.return_value = [mock_country]

        response = self.client.get('/countries')

        self.assertEqual(response.status_code, 200)

    @patch('api.country_api.pycountry.countries')
    def test_get_country(self, MockCountries):
        mock_country = MagicMock()
        mock_country.name = "United States"
        mock_country.alpha_2 = "US"
        MockCountries.get.return_value = mock_country

        response = self.client.get('/countries/US')

        self.assertEqual(response.status_code, 200)

    @patch('api.country_api.get_cities_by_country')
    @patch('api.country_api.pycountry.countries')
    def test_get_country_cities(self, MockCountries, MockGetCities):
        mock_country = MagicMock()
        mock_country.name = "United States"
        mock_country.alpha_2 = "US"
        MockCountries.get.return_value = mock_country
        MockGetCities.return_value = [{"name": "New York", "id": "US"}]

        response = self.client.get('/countries/US/cities')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [{"name": "New York", "id": "US"}])


if __name__ == '__main__':
    unittest.main()
