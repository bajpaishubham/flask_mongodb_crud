# Necessary imports
from flask import Flask, request, jsonify
from bson.objectid import ObjectId
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth

# Create a Flask application
app = Flask(__name__)
auth = HTTPBasicAuth()

try:
    # Create a MongoClient to the running mongod instance
    # If issues arise, check the status of the mongod process using: sudo systemctl status mongod
    # Start the mongod process if not running using: sudo systemctl start mongod
    # Docker
    client = MongoClient("mongo", 27017)
    # Access the database
    db = client['json_db']
    # Access the collection
    collection = db['data']
except errors.ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")

# Authentication
# Sample users for authentication
users = {
    "admin": generate_password_hash("password")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@auth.error_handler
def auth_error(status):
    return {"error":"Incorrect credentials"}, 401


# For the APIs try except blocks are used for exception handling
# and if else blocks are used to handle missing data and invalid JSON

"""
    Welcome endpoint: GET /: Provides result for the default url

    Example Response:
    {
        "Hello User": "Welcome to the application for CRUD operations on a JSON database"
    }
"""
@app.route('/', methods=['GET'])
@auth.login_required
def welcome():
    return jsonify({'Hello User':'Welcome to the application for CRUD operations on a JSON database'}), 200

"""
    Create data endpoint: POST /data: Accepts a JSON object and stores it in the database

    Example Request:
    POST /data
    {
        "name": "John",
        "age": 30,
        "city": "New York"
    }

    Example Response:
    {
        "id": "60c72b2f4f1a2c1a4c8b4567"
    }
"""
@app.route('/data', methods=['POST'])
@auth.login_required
def create_data():
    try:
        if not request.is_json:
            return jsonify({"error": "Request body must be JSON"}), 400

        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing data"}), 400

        result = collection.insert_one(data)
        return jsonify({'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

"""
    Get data by ID endpoint: GET /data/{id}: Retrieves the JSON object associated with the given ID from the database

    Example Request:
    GET /data/60c72b2f4f1a2c1a4c8b4567

    Example Response:
    {
        "_id": "60c72b2f4f1a2c1a4c8b4567",
        "name": "John",
        "age": 30,
        "city": "New York"
    }
"""
@app.route('/data/<id>', methods=['GET'])
@auth.login_required
def get_data(id):
    try:
        object_id = ObjectId(id)
    except Exception as e:
        return jsonify({"error": "Invalid ID format"}), 400
    
    try:
        data = collection.find_one({'_id': ObjectId(id)})
        if data:
            data['_id'] = str(data['_id'])
            return jsonify(data), 200
        else:
            return jsonify({'error': 'Data not found for this id'}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

"""
    Update data by ID endpoint: PUT /data/{id}: Updates the existing JSON object with the given ID in the database

    Example Request:
    PUT /data/60c72b2f4f1a2c1a4c8b4567
    {
        "name": "Jane",
        "age": 25,
        "city": "Los Angeles"
    }

    Example Response:
    {
        "message": "Data updated successfully"
    }
"""
@app.route('/data/<id>', methods=['PUT'])
@auth.login_required
def update_data(id):
    try:
        object_id = ObjectId(id)
    except Exception as e:
        return jsonify({"error": "Invalid ID format"}), 400
    
    try:
        if not request.is_json:
            return jsonify({"error": "Request body must be JSON"}), 400

        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing data"}), 400

        result = collection.update_one({'_id': ObjectId(id)}, {'$set': data})
        if result.matched_count:
            return jsonify({'message': 'Data updated successfully'}), 200
        else:
            return jsonify({'error': 'Data not found for this id'}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

"""
    Delete data by ID endpoint: DELETE /data/{id}: Deletes the JSON object with the given ID from the database

    Example Request:
    DELETE /data/60c72b2f4f1a2c1a4c8b4567

    Example Response:
    {
        "message": "Data deleted successfully"
    }
"""
@app.route('/data/<id>', methods=['DELETE'])
@auth.login_required
def delete_data(id):
    try:
        object_id = ObjectId(id)
    except Exception as e:
        return jsonify({"error": "Invalid ID format"}), 400
    
    try:
        result = collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count:
            return jsonify({'message': 'Data deleted successfully'}), 200
        else:
            return jsonify({'error': 'Data not found for this id'}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
