from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['Job_Listing']  
collection = db['Job_Listing_data']

@app.route('/data', methods=['GET'])
def get_all_data():
    data = list(collection.find({}, {'_id': False}))  
    return jsonify(data)


@app.route('/data/add', methods=['POST'])
def insert_data():
    new_data = request.get_json()  
    if new_data:
        collection.insert_one(new_data)
        return jsonify({'message': 'Data inserted successfully'}), 201
    else:
        return jsonify({'error': 'No data provided'}), 400

@app.route('/data/filter', methods=['GET'])
def filter_data():
    column = request.args.get('Comapny-Name')  
    value = request.args.get('Accenture')   
    
    if column and value:
        data = list(collection.find({column: value}, {'_id': False}))
        if data:
            return jsonify(data)
        else:
            return jsonify({'error': 'No matching data found'}), 404
    else:
        return jsonify({'error': 'Invalid query'}), 400

if __name__ == '__main__':
    app.run(debug=True)
