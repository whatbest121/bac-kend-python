from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient
from flasgger import Swagger, swag_from

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'test'

# เชื่อมต่อ MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['best']
collection = db['test']

jwt = JWTManager(app)
swagger = Swagger(app)

def create_token(username):
    # สร้าง access token
    access_token = create_access_token(identity=username)
    # เก็บ token ในคอลเลคชัน MongoDB
    collection.insert_one({"username": username, "token": access_token})
    return access_token

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

    # ตรวจสอบข้อมูลการเข้าสู่ระบบ
    if username == 'admin' and password == '1234':
        access_token = create_token(username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/data', methods=['GET'])
@jwt_required()
@swag_from('swagger_doc.yaml')
def get_data():
    """
    Get All Data Endpoint
    ---
    responses:
      200:
        description: A list of all data retrieved successfully
        
    """
    # ดึงค่า token จาก Flask-JWT context
    token = request.headers.get('Authorization').split(' ')[1]

    if token:
        response = requests.get('http://localhost:5000/data', headers={'Authorization': f'Bearer {token}'})
        return jsonify(response.json()), response.status_code
    else:
        return jsonify({"message": "Token is not set"}), 401
    
@app.route('/data', methods=['POST'])
@jwt_required()
def add_data():
    """
    Add Data Endpoint
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
          
            name:
              type: string
            value:
              type: integer
    responses:
      201:
        description: Data added successfully
    """
    new_data = request.get_json()
    collection.insert_one(new_data)
    return jsonify({"message": "Data added successfully"}), 201

@app.route('/data/<id>', methods=['PUT'])
@jwt_required()
def update_data(id):
    """
    Update Data Endpoint
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: string
        description: ID of the data to be updated
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            value:
              type: integer
    responses:
      200:
        description: Data updated successfully
    """
    updated_data = request.get_json()
    collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
    return jsonify({"message": "Data updated successfully"}), 200

@app.route('/data/<id>', methods=['DELETE'])
@jwt_required()
def delete_data(id):
    """
    Delete Data Endpoint
    ---
    parameters:
      - name: id
        in: path
        required: true
        type: string
        description: ID of the data to be deleted
    responses:
      200:
        description: Data deleted successfully
    """
    collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Data deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
