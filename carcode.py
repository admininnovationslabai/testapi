from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample car data
cars = [
    {"id": 1, "name": "Toyota Camry", "make": "Toyota", "model": "Camry", "year": 2022, "price": 24999},
    {"id": 2, "name": "Honda Accord", "make": "Honda", "model": "Accord", "year": 2023, "price": 26999},
    {"id": 3, "name": "Ford Mustang", "make": "Ford", "model": "Mustang", "year": 2021, "price": 39999},
    {"id": 4, "name": "Chevrolet Malibu", "make": "Chevrolet", "model": "Malibu", "year": 2020, "price": 21999},
    {"id": 5, "name": "BMW 3 Series", "make": "BMW", "model": "3 Series", "year": 2022, "price": 42999}
]

@app.route('/cars', methods=['GET'])
def get_cars():
    
        # Get query parameters
        sort_by = request.args.get('sort_by', default='price')  # Default is by price
        sort_order = request.args.get('sort_order', default='asc')  # Default is ascending
        id_filter = request.args.get('id', type=int)  # Filter by ID
        name_search = request.args.get('name', type=str)  # Partial name search

        # Validate sort_by parameter
        if sort_by not in ['price', 'year']:
            return jsonify({"error": "Invalid 'sort_by' value. Valid values are 'price' or 'year'."}), 400

        # Validate sort_order parameter
        if sort_order not in ['asc', 'desc']:
            return jsonify({"error": "Invalid 'sort_order' value. Valid values are 'asc' or 'desc'."}), 400

        filtered_cars = cars

        # Filter by ID if provided
        if id_filter:
            filtered_cars = [car for car in filtered_cars if car['id'] == id_filter]

        # Filter by partial name search if provided
        if name_search:
            filtered_cars = [car for car in filtered_cars if name_search.lower() in car['name'].lower()]

        if not filtered_cars:
         return jsonify({"error":"car doesn't found"}), 404
        
        # Sorting based on sort_by and sort_order
        reverse = True if sort_order == 'desc' else False
        filtered_cars = sorted(filtered_cars, key=lambda x: x[sort_by], reverse=reverse)
        
        return jsonify(filtered_cars)

        

if __name__ == '__main__':
    app.run(debug=True)