import os
import unittest
import json
from app import app, db
from models.users import User

class TestProductionDatabaseOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config.from_object('config.ProductionConfig')
        cls.app = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def setUp(self):
        with app.app_context():
            db.session.commit()  # Commit any changes to the database
            db.session.remove()   # Remove any existing sessions

    def tearDown(self):
        pass  # No additional cleanup needed for each test

    def test_create_user(self):
        """Test creating a new user."""
        data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password'
        }
        response = self.app.post('/users', json=data)
        self.assertEqual(response.status_code, 201)  # HTTP 201 Created
        self.assertIn('id', response.json)  # Ensure the response contains an ID

    def test_update_user(self):
        """Test updating a user."""
        user = User(email='test@example.com', first_name='John', last_name='Doe', password='password')
        with app.app_context():
            db.session.add(user)
            db.session.commit()

            saved_user = User.query.filter_by(email='test@example.com').first()
            data = {
                'email': 'updated@example.com'
            }
            response = self.app.put(f'/users/{saved_user.id}', json=data)
            self.assertEqual(response.status_code, 200)  # HTTP 200 OK
            self.assertEqual(response.json['email'], 'updated@example.com')

    def test_delete_user(self):
        """Test deleting a user."""
        user = User(email='test@example.com', first_name='John', last_name='Doe', password='password')
        with app.app_context():
            db.session.add(user)
            db.session.commit()

            saved_user = User.query.filter_by(email='test@example.com').first()
            response = self.app.delete(f'/users/{saved_user.id}')
            self.assertEqual(response.status_code, 204)  # HTTP 204 No Content

            # Verify user is deleted from the database
            deleted_user = User.query.get(saved_user.id)
            self.assertIsNone(deleted_user, "User was not deleted from the database.")

if __name__ == '__main__':
    unittest.main()
