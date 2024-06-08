import unittest
import json
from application import app, collection  # Import the Flask app and MongoDB collection
from bson.objectid import ObjectId
from pymongo import MongoClient
from base64 import b64encode
from werkzeug.security import generate_password_hash

class ApplicationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup MongoDB client and test database."""
        cls.client = MongoClient("mongo", 27017)
        cls.db = cls.client['json_db']
        cls.collection = cls.db['data']
        
        # Setup Flask app
        cls.app = app.test_client()
        cls.app.testing = True

        # Insert sample data for testing
        cls.sample_data = {"name": "John", "age": 30, "city": "New York"}
        cls.sample_data_id = cls.collection.insert_one(cls.sample_data).inserted_id
        
        cls.sample_data_2 = {"name": "Kohl", "age": 20, "city": "New Jersey"}
        cls.sample_data_id_2 = cls.collection.insert_one(cls.sample_data_2).inserted_id

        # Set up basic authentication credentials
        cls.username = "admin"
        cls.password = "password"
        cls.auth_header = 'Basic ' + b64encode(('admin:password').encode('utf-8')).decode('utf-8')
        cls.auth_header_2 = 'Basic ' + b64encode(('admin:wrong_password').encode('utf-8')).decode('utf-8')
        cls.auth_header_3 = 'Basic ' + b64encode(('anon_user:password').encode('utf-8')).decode('utf-8')
        cls.auth_header_4 = 'Basic ' + b64encode(('anon_user:wrong_password').encode('utf-8')).decode('utf-8')

    @classmethod
    def tearDownClass(cls):
        """Cleanup MongoDB collection after tests are done."""
        cls.collection.drop()
        cls.client.close()

    def get_authenticated_client(self):
        """Return a test client with basic authentication headers."""
        return self.app.open('/',
                              method='GET',
                              headers={'Authorization': self.auth_header})

    # Test the welcome endpoint
    def test_welcome(self):
        response = self.app.get('/', headers={'Authorization': self.auth_header})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'Hello User': 'Welcome to the application for CRUD operations on a JSON database'})
    
    # Test authentication with incorrect credentials
    def test_welcome_unauthenticated_user(self):
        response = self.app.get('/', headers={'Authorization': self.auth_header_2})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {'error': 'Incorrect credentials'})

        response = self.app.get('/', headers={'Authorization': self.auth_header_3})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {'error': 'Incorrect credentials'})

        response = self.app.get('/', headers={'Authorization': self.auth_header_4})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {'error': 'Incorrect credentials'})

    # Test the data creation endpoint
    def test_create_data(self):
        new_data = {"name": "Alice", "age": 28, "city": "Los Angeles", "height": 6}
        response = self.app.post('/data', json=new_data, headers={'Authorization': self.auth_header})
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        created_id = ObjectId(response.json['id'])
        
        # Verify that data is correctly inserted into the database
        created_data = self.collection.find_one({"_id": created_id})
        self.assertIsNotNone(created_data)
        self.assertEqual(created_data['name'], new_data['name'])

    # Test fetching data with a valid ID
    def test_get_data_valid_id(self):
        response = self.app.get(f'/data/{self.sample_data_id}', headers={'Authorization': self.auth_header})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['_id'], str(self.sample_data_id))
        self.assertEqual(response.json['name'], self.sample_data['name'])

    # Test fetching data with an invalid ID format
    def test_get_data_invalid_id(self):
        response = self.app.get('/data/invalid_id', headers={'Authorization': self.auth_header})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Invalid ID format"})

    # Test fetching data with a non-existent ID
    def test_get_data_not_found(self):
        non_existent_id = ObjectId()
        response = self.app.get(f'/data/{non_existent_id}', headers={'Authorization': self.auth_header})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Data not found for this id"})

    # Test updating data with a valid ID
    def test_update_data(self):
        update_data = {"name": "Jane", "age": 25, "city": "Los Angeles"}
        response = self.app.put(f'/data/{self.sample_data_id}', json=update_data, headers={'Authorization': self.auth_header})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Data updated successfully"})
        
        # Verify that data is correctly updated in the database
        updated_data = self.collection.find_one({"_id": self.sample_data_id})
        self.assertEqual(updated_data['name'], update_data['name'])

    # Test updating data with an invalid ID format
    def test_update_data_invalid_id(self):
        response = self.app.put('/data/invalid_id', json={"name": "Test"}, headers={'Authorization': self.auth_header})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Invalid ID format"})

    # Test updating data with a non-existent ID
    def test_update_data_not_found(self):
        non_existent_id = ObjectId()
        response = self.app.put(f'/data/{non_existent_id}', json={"name": "Test"}, headers={'Authorization': self.auth_header})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Data not found for this id"})

    # Test deleting data with a valid ID
    def test_delete_data(self):
        response = self.app.delete(f'/data/{self.sample_data_id_2}', headers={'Authorization': self.auth_header})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Data deleted successfully"})
        
        # Verify that data is correctly deleted from the database
        deleted_data = self.collection.find_one({"_id": self.sample_data_id_2})
        self.assertIsNone(deleted_data)

    # Test deleting data with an invalid ID format
    def test_delete_data_invalid_id(self):
        response = self.app.delete('/data/invalid_id', headers={'Authorization': self.auth_header})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Invalid ID format"})

    # Test deleting data with a non-existent ID
    def test_delete_data_not_found(self):
        non_existent_id = ObjectId()
        response = self.app.delete(f'/data/{non_existent_id}', headers={'Authorization': self.auth_header})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Data not found for this id"})

if __name__ == '__main__':
    unittest.main()
