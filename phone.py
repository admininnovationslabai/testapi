from flask import Flask, request, jsonify
import json

app = Flask(__name__)

phones = [
    {"id": 1, "name": "iPhone 13", "brand": "Apple", "price": 999},
    {"id": 2, "name": "Samsung Galaxy S21", "brand": "Samsung", "price": 799},
    {"id": 3, "name": "OnePlus 9", "brand": "OnePlus", "price": 729},
    {"id": 4, "name": "Google Pixel 6", "brand": "Google", "price": 599},
    {"id": 5, "name": "Xiaomi Mi 11", "brand": "Xiaomi", "price": 699}
]

@app.route('/phones', methods=['GET'])
def get_phones():
    query_id = request.args.get('id', type=int)
    query_name = request.args.get('name', '').lower()
    sort_by = request.args.get('sort', 'id')

    filtered_phones = phones
    
    if query_id:
        filtered_phones = [phone for phone in phones if phone["id"] == query_id]
    elif query_name:
        filtered_phones = [phone for phone in phones if query_name in phone["name"].lower()]
    
    if sort_by in ['id', 'price']:
        filtered_phones = sorted(filtered_phones, key=lambda x: x[sort_by])
    
    return jsonify(filtered_phones[:5])


if __name__ == '__main__':
    app.run(debug=True)
