from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
uri = "mongodb+srv://Salman:PGmZaVVguCzcedmt@cucalun.uhxfh.mongodb.net/?retryWrites=true&w=majority&appName=CuCaLun"

# Koneksi ke MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["sensor_database"]
collection = db["sensor_data"]

@app.route("/sensor-data", methods=["POST"])
def receive_data():
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400
    
    collection.insert_one(data)
    return jsonify({"message": "Data stored successfully"}), 201

@app.route('/sensor-data', methods=['GET'])
def get_data():return "Hello, World!"
if __name__ == "__main__":
    app.run(debug=True)
