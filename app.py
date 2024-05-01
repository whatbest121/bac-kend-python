from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, set_access_cookies
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

app.config['SWAGGER'] = {
    'swagger': '2.0',
    'securityDefinitions': {
        'JWTAuth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
}

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
        response = jsonify(access_token=access_token)
        set_access_cookies(response, access_token)
        return response, 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401
@app.route('/data', methods=['GET'])
# @jwt_required()
@swag_from({
    'security': [{'JWTAuth': []}],
    'parameters': [],
    'responses': {
        200: {
            'description': 'Data retrieved successfully'
        }
    }
})
def get_data():
    """
    Get Data Endpoint
    ---
    security:
      - JWTAuth: []
    responses:
      200:
        description: Data retrieved successfully
    """
    try:
        data = list(collection.find())
        for item in data:
            item['_id'] = str(item['_id'])
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 401

@app.route('/data', methods=['POST'])
def add_data():
    """
    Add Data Endpoint
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            Seed_Crop_Year:
              type: string
            Seed_RDCSD:
              type: string
            Seed_RepDate:
              type: string
            Seed_Season:
              type: string
            Seed_Stock2Sale:
              type: string
            Seed_Variety:
              type: string
            Seed_Year:
              type: string
            Seeds_YearWeek:
              type: string
    responses:
      201:
        description: Data added successfully
    """
    try:
        if request.content_type == 'application/json':
            new_data = request.get_json()
            result = collection.insert_one(new_data)
            return jsonify({"message": "Data added successfully", "inserted_id": str(result.inserted_id)}), 201
        else:
            return jsonify({"message": "Unsupported Media Type: Request Content-Type must be 'application/json'"}), 415
    except Exception as e:
        return jsonify({"message": str(e)}), 500
@app.route('/data/<id>', methods=['PUT'])
# @jwt_required()
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The ID of the data to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'description': 'Data to update',
            'schema': {
                'type': 'object',
                'properties': {
                    'Seed_Crop _Year': {'type': 'string'},
                    'Seed_RDCSD': {'type': 'string'},
                    'Seed_RepDate': {'type': 'string'},
                    'Seed_Season': {'type': 'string'},
                    'Seed_Stock2Sale': {'type': 'string'},
                    'Seed_Varity': {'type': 'string'},
                    'Seed_Year': {'type': 'string'},
                    'Seeds_YearWeek': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Data updated successfully'
        }
    }
})
def update_data(id):
    """
    Update Data Endpoint
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The ID of the data to update
      - name: body
        in: body
        description: Data to update
        schema:
          type: object
          properties:
            Seed_Crop _Year:
              type: string
            Seed_RDCSD:
              type: string
            Seed_RepDate:
              type: string
            Seed_Season:
              type: string
            Seed_Stock2Sale:
              type: string
            Seed_Varity:
              type: string
            Seed_Year:
              type: string
            Seeds_YearWeek:
              type: string
    responses:
      200:
        description: Data updated successfully
    """
    try:
        if request.content_type == 'application/json':  # Check Content-Type
            updated_data = request.get_json()

            existing_data = collection.find_one({"_id": ObjectId(id)})

            updated_fields = {k: v for k, v in updated_data.items() if k in existing_data}

            collection.update_one({"_id": ObjectId(id)}, {"$set": updated_fields})
            return jsonify({"message": "Data updated successfully"}), 200
        else:
            return jsonify({"message": "Unsupported Media Type: Request Content-Type must be 'application/json'"}), 415
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/data/<id>', methods=['DELETE'])
# @jwt_required()
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The ID of the data to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Data deleted successfully'
        }
    }
})
def delete_data(id):
    """
    Delete Data Endpoint
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The ID of the data to delete
    responses:
      200:
        description: Data deleted successfully
    """
    collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Data deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
