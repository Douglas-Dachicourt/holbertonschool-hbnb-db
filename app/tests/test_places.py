import unittest
from flask import Flask
from flask.testing import FlaskClient
from api.place_api import place_api
from models.place import Place
from persistence.datamanager import DataManager
from unittest.mock import patch, MagicMock
import json

class PlaceApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(place_api)
        self.app.testing = True
        self.client = self.app.test_client()
        self.client: FlaskClient

    @patch('api.place_api.DataManager')
    def test_add_place_missing_field(self, MockDataManager):
        response = self.client.post('/places', json={
            "name": "Beach House",
            "description": "A beautiful beach house"
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required field', response.get_json()['Error'])

    @patch('api.place_api.DataManager')
    def test_add_place_invalid_type(self, MockDataManager):
        response = self.client.post('/places', json={
            "name": "Beach House",
            "description": "A beautiful beach house",
            "address": "123 Ocean Drive",
            "latitude": "invalid",
            "longitude": -118.2437,
            "num_rooms": 3,
            "num_bathrooms": 2,
            "price_per_night": 200,
            "max_guests": 6,
            "host_id": "1",
            "city_id": "1",
            "amenity_ids": ["1"]
        })

        self.assertEqual(response.status_code, 409)

    @patch('api.place_api.DataManager')
    def test_get_places(self, MockDataManager):
        with patch('builtins.open', unittest.mock.mock_open(read_data='[{"name": "Beach House"}]')):
            response = self.client.get('/places')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), [{"name": "Beach House"}])

    @patch('api.place_api.DataManager')
    def test_get_places_file_not_found(self, MockDataManager):
        with patch('builtins.open', side_effect=FileNotFoundError):
            response = self.client.get('/places')

            self.assertEqual(response.status_code, 404)
            self.assertIn('No place found', response.get_json()['Error'])

    @patch('api.place_api.DataManager')
    def test_get_place_by_id_not_found(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = None

        response = self.client.get('/places/1')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Place not found', response.get_json()['Error'])

    @patch('api.place_api.DataManager')
    def test_delete_place_not_found(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = None

        response = self.client.delete('/places/1')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Place not found', response.get_json()['Error'])



    @patch('api.place_api.DataManager')
    def test_update_place_not_found(self, MockDataManager):
        mock_datamanager = MockDataManager.return_value
        mock_datamanager.get.return_value = None

        response = self.client.put('/places/1', json={
            "name": "Updated Beach House",
            "description": "An updated description",
            "address": "123 Ocean Drive",
            "latitude": 34.0522,
            "longitude": -118.2437,
            "num_rooms": 3,
            "num_bathrooms": 2,
            "price_per_night": 250,
            "max_guests": 6,
            "host_id": "1",
            "city_id": "1",
            "amenity_ids": ["1"]
        })

        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', response.get_json()['Error'])


if __name__ == '__main__':
    unittest.main()
