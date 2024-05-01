from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from pymongo import MongoClient
from flasgger import Swagger, swag_from
from bson import ObjectId 

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'test'

client = MongoClient('mongodb://localhost:27017/')
db = client['best'] 
collection = db['test']

swagger = Swagger(app)
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    """
    User Login Endpoint
    ---
    parameters:
      - name: username
        in: formData
        type: string
        required: true
        description: The username for login
      - name: password
        in: formData
        type: string
        required: true
        description: The password for login
    responses:
      200:
        description: User logged in successfully
        examples:
          access_token: "JWT access token"
      401:
        description: Invalid username or password
    """
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    if username == 'admin' and password == '1234':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/data', methods=['GET'])
@jwt_required()
@swag_from('swagger_doc.yml')
def get_data():
    try:
        data = list(collection.find())
        for item in data:
            item['_id'] = str(item['_id'])
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 401

@app.route('/data', methods=['POST'])
@jwt_required()
def add_data():
    new_data = request.get_json()
    collection.insert_one(new_data)
    return jsonify({"message": "Data added successfully"}), 201

@app.route('/data/<id>', methods=['PUT'])
@jwt_required()
def update_data(id):
    updated_data = request.get_json()
    collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
    return jsonify({"message": "Data updated successfully"}), 200

@app.route('/data/<id>', methods=['DELETE'])
@jwt_required()
def delete_data(id):
    collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Data deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
