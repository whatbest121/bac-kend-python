from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from pymongo import MongoClient
import csv

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'test'

# เชื่อมต่อ MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['best'] 
collection = db['test']

jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)


    if username == 'admin' and password == '1234':

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

# สร้าง API Get Data
@app.route('/data', methods=['GET'])
@jwt_required()
def get_data():
    data = list(collection.find())
    for item in data:
        item['_id'] = str(item['_id'])
    return jsonify(data), 200

# สร้าง API Add Data
@app.route('/data', methods=['POST'])
@jwt_required()
def add_data():
    new_data = request.get_json()
    collection.insert_one(new_data)
    return jsonify({"message": "Data added successfully"}), 201

# สร้าง API Update Data
@app.route('/data/<id>', methods=['PUT'])
@jwt_required()
def update_data(id):
    updated_data = request.get_json()
    collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
    return jsonify({"message": "Data updated successfully"}), 200

# สร้าง API Delete Data
@app.route('/data/<id>', methods=['DELETE'])
@jwt_required()
def delete_data(id):
    collection.delete_one({"_id": (id)})
    return jsonify({"message": "Data deleted successfully"}), 200
if __name__ == '__main__':
    app.run(debug=True, port=5000)