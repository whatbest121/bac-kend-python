from flask import Flask, jsonify, request
from pymongo import MongoClient
import csv

app = Flask(__name__)

# เชื่อมต่อ MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['best'] 
collection = db['test']

# สร้าง API Get Data
@app.route('/data', methods=['GET'])
def get_data():
    data = list(collection.find())
    for item in data:
        item['_id'] = str(item['_id'])
    return jsonify(data), 200

# สร้าง API Add Data
@app.route('/data', methods=['POST'])
def add_data():
    new_data = request.get_json()
    collection.insert_one(new_data)
    return jsonify({"message": "Data added successfully"}), 201

# สร้าง API Update Data
@app.route('/data/<id>', methods=['PUT'])
def update_data(id):
    updated_data = request.get_json()
    collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
    return jsonify({"message": "Data updated successfully"}), 200

# สร้าง API Delete Data
@app.route('/data/<id>', methods=['DELETE'])
def delete_data(id):
    collection.delete_one({"_id": (id)})
    return jsonify({"message": "Data deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)