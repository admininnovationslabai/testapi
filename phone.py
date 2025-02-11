from flask import Flask, request, jsonify

app = Flask(__name__)

phones = [
    {"id": 1, "name": "iPhone 13", "brand": "Apple", "price": 999},
    {"id": 2, "name": "Samsung Galaxy S21", "brand": "Samsung", "price": 799},
    {"id": 3, "name": "OnePlus 9", "brand": "OnePlus", "price": 729},
    {"id": 4, "name": "Google Pixel 6", "brand": "Google", "price": 5599},
    {"id": 5, "name": "Xiaomi Mi 11", "brand": "Xiaomi", "price": 6699}
]

@app.route('/phones', methods=['GET'])
def get_phones():
    query_id = request.args.get('id', type=int)
    query_name = request.args.get('name', '').lower()
    query_brand = request.args.get('brand', '').lower()  # New: Filter by brand
    min_price = request.args.get('min_price', type=int)  # New: Min price filter
    max_price = request.args.get('max_price', type=int)  # New: Max price filter
    sort= request.args.get("sort", type=str)
    order = request.args.get("order", type=str, default="asc") 

    filtered_phones = phones
    
    if query_id:
        filtered_phones = [phone for phone in phones if phone["id"] == query_id]
    elif query_name:
        filtered_phones = [phone for phone in phones if query_name in phone["name"].lower()]

    if query_brand:
        filtered_phones = [phone for phone in filtered_phones if phone["brand"].lower() == query_brand]
    
    if min_price is not None:
        filtered_phones = [phone for phone in filtered_phones if phone["price"] >= min_price]
    
    if max_price is not None:
        filtered_phones = [phone for phone in filtered_phones if phone["price"] <= max_price]
   
    if not filtered_phones:
        return jsonify({"message": "No phones found"}), 404  
    
    # Sorting (Case-Insensitive)
    if sort in ["name", "brand", "price"]:
        reverse_order = True if order.lower() == "desc" else False
        if sort == "name":
            filtered_phones = sorted(filtered_phones, key=lambda x: x["name"].lower(), reverse=reverse_order)
        else:
            filtered_phones = sorted(filtered_phones, key=lambda x: x[sort], reverse=reverse_order)
        if sort == "brand":
            filtered_phones = sorted(filtered_phones, key=lambda x: x["brand"].lower(), reverse=reverse_order)
        else:
            filtered_phones = sorted(filtered_phones, key=lambda x: x[sort], reverse=reverse_order)
        if sort == "price":
            filtered_phones = sorted(filtered_phones, key=lambda x: x["price"], reverse=reverse_order)
        else:
            filtered_phones = sorted(filtered_phones, key=lambda x: x[sort], reverse=reverse_order)

    
    return jsonify(filtered_phones[:5])

if __name__ == '__main__':
    app.run(debug=True)

