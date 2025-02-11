import json
from flask import Flask, jsonify, request

app = Flask(__name__)

dogs = [
    {"id": 1, "name": "Ramu"},
    {"id": 2, "name": "Somu"},
    {"id": 3, "name": "Raju"},
    {"id": 4, "name": "Jiju"},
    {"id": 5, "name": "siju"}
]

@app.route('/dogs', methods=['GET'])
def get_dogs():
    name_search = request.args.get('name', '').lower()   # it'll extract the name query paramter
    sort_by_id = request.args.get('sort_by') == "id"    # extract sort by query parameter
    
    filtered_dogs = [dog for dog in dogs if name_search in dog['name'].lower()]  #returns the name of the dogs mentioned in search string and case sensitive
    
    if sort_by_id:    #sort by id
        filtered_dogs.sort(key=lambda x: x['id'])  #it extarcts id value from each dictionary in asc
    
    return jsonify(filtered_dogs)

@app.route('/dogs/<int:id>', methods=['GET'])
def get_dog(id: int):
    dog = next((d for d in dogs if d['id'] == id), None)
    return jsonify(dog) if dog else (jsonify({'error': 'Dog not found.'}), 404)

if __name__ == '__main__':
    app.run(port=5000)
