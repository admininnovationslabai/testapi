import json
from flask import Flask, jsonify, request

app = Flask(__name__)

dogs = [
    {"id": 1, "name": "Buddy"},
    {"id": 2, "name": "Charlie"},
    {"id": 3, "name": "Max"},
    {"id": 4, "name": "Rocky"},
    {"id": 5, "name": "Bella"}
]

@app.route('/dogs', methods=['GET'])
def get_dogs():
    name_search = request.args.get('name', '').lower()
    sort_by_id = request.args.get('sort_by') == "id"
    
    filtered_dogs = [dog for dog in dogs if name_search in dog['name'].lower()]
    
    if sort_by_id:
        filtered_dogs.sort(key=lambda x: x['id'])
    
    return jsonify(filtered_dogs)

@app.route('/dogs/<int:id>', methods=['GET'])
def get_dog(id: int):
    dog = next((d for d in dogs if d['id'] == id), None)
    return jsonify(dog) if dog else (jsonify({'error': 'Dog not found.'}), 404)

if __name__ == '__main__':
    app.run(port=5000)
