from flask import Flask, request, jsonify, abort
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Simulated data store (this could represent a database in a real application)
users = [
    {"id": 1, "name": "Alice", "age": 30, "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "age": 25, "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "age": 35, "email": "charlie@example.com"},
    {"id": 4, "name": "David", "age": 28, "email": "david@example.com"}
]

@app.route('/users', methods=['GET'])
def get_users():
    try:
        # Retrieve optional query parameters
        user_id = request.args.get('id', type=int)
        name = request.args.get('name', type=str)
        min_age = request.args.get('min_age', type=int)
        max_age = request.args.get('max_age', type=int)
        sort_by = request.args.get('sort_by', type=str)  # Can be 'id', 'name', or 'age'

        # Start with the full list of users
        filtered_users = users

        # Filter by user ID if provided
        if user_id is not None:
            filtered_users = [user for user in filtered_users if user['id'] == user_id]

        # Filter by name substring if provided (case-insensitive search)
        if name:
            filtered_users = [user for user in filtered_users if name.lower() in user['name'].lower()]

        # Filter by minimum age if provided
        if min_age is not None:
            filtered_users = [user for user in filtered_users if user['age'] >= min_age]

        # Filter by maximum age if provided
        if max_age is not None:
            filtered_users = [user for user in filtered_users if user['age'] <= max_age]

        # Apply sorting if requested
        if sort_by:
            if sort_by in ['id', 'name', 'age']:
                filtered_users = sorted(filtered_users, key=lambda x: x[sort_by])
            else:
                # Return an error if sort_by parameter is invalid
                return jsonify({"error": "Invalid sort_by parameter. Valid options: 'id', 'name', 'age'."}), 400

        # Return a 404 if no users match the criteria
        if not filtered_users:
            return jsonify({"message": "No users found matching the criteria."}), 404

        return jsonify({"users": filtered_users}), 200

    except Exception as e:
        app.logger.error(f"Error processing GET /users: {str(e)}")
        abort(500, description="Internal Server Error")


#Dinosaurs GET API

dinosaurs = [
    {"id": 1, "name": "Tyrannosaurus Rex", "diet": "Carnivore", "length": "12m", "weight": "8000kg"},
    {"id": 2, "name": "Velociraptor", "diet": "Carnivore", "length": "2m", "weight": "15kg"},
    {"id": 3, "name": "Triceratops", "diet": "Herbivore", "length": "9m", "weight": "6000kg"},
    {"id": 4, "name": "Brachiosaurus", "diet": "Herbivore", "length": "22m", "weight": "56000kg"},
    {"id": 5, "name": "Stegosaurus", "diet": "Herbivore", "length": "9m", "weight": "5000kg"}
]


@app.route("/dinosaurs", methods=["GET"])
def get_dinosaurs():
    id_filter = request.args.get("id")
    name_filter = request.args.get("name")
    diet_filter = request.args.get("diet")
    length_filter = request.args.get("length")
    weight_filter = request.args.get("weight")
    sort_order = request.args.get("sort")

    filtered_dinosaurs = dinosaurs

    # Validate and filter by ID
    if id_filter:
        if not id_filter.isdigit():
            return jsonify({"error": "Invalid ID. It must be a number."}), 400
        filtered_dinosaurs = [d for d in filtered_dinosaurs if d["id"] == int(id_filter)]
        if not filtered_dinosaurs:
            return jsonify({"error": f"No dinosaur found with ID {id_filter}"}), 404

    # Validate and filter by Name (partial match)
    if name_filter:
        filtered_dinosaurs = [d for d in filtered_dinosaurs if name_filter.lower() in d["name"].lower()]
        if not filtered_dinosaurs:
            return jsonify({"error": f"No dinosaur found with name containing '{name_filter}'"}), 404

    # Validate and filter by Diet (exact match)
    if diet_filter:
        filtered_dinosaurs = [d for d in filtered_dinosaurs if d["diet"].lower() == diet_filter.lower()]
        if not filtered_dinosaurs:
            return jsonify({"error": f"No dinosaur found with diet '{diet_filter}'"}), 404

    # Validate and filter by Length (exact match)
    if length_filter:
        filtered_dinosaurs = [d for d in filtered_dinosaurs if d["length"] == length_filter]
        if not filtered_dinosaurs:
            return jsonify({"error": f"No dinosaur found with length '{length_filter}'"}), 404

    # Validate and filter by Weight (exact match)
    if weight_filter:
        filtered_dinosaurs = [d for d in filtered_dinosaurs if d["weight"] == weight_filter]
        if not filtered_dinosaurs:
            return jsonify({"error": f"No dinosaur found with weight '{weight_filter}'"}), 404

    # Validate and apply sorting by Name
    if sort_order:
            if sort_order not in ["asc", "desc"]:
                return jsonify({"error": "Invalid sort order. Use 'asc' or 'desc'."}), 400

            def sort_by_name(dino):
                return dino["name"]

            filtered_dinosaurs.sort(key=sort_by_name, reverse=(sort_order == "desc"))

    return jsonify(filtered_dinosaurs)


#cities api code

cities = [
    {"id": 1, "name": "Tokyo", "country": "Japan", "population": 8419600},
    {"id": 2, "name": "Los Angeles", "country": "USA", "population": 3980400},
    {"id": 3, "name": "Paris", "country": "France", "population": 2716000},
    {"id": 4, "name": "Berlin", "country": "Germany", "population": 2328000},
    {"id": 5, "name": "kerala", "country": "India", "population": 1690000}
]
@app.route('/cities', methods=['GET'])
def get_cities():
    # Get query parameters
    id = request.args.get("id", type=int)
    name = request.args.get("name", type=str)
    country = request.args.get("country", type=str)
    sort= request.args.get("sort", type=str)
    order = request.args.get("order", type=str, default="asc")  
    min_population = request.args.get("minPopulation", type=int)
    max_population = request.args.get("maxPopulation", type=int)

   
    filtered_cities = cities

    if id:
        filtered_cities = [city for city in filtered_cities if city["id"] == id]
    
    if name:
        filtered_cities = [city for city in filtered_cities if name.lower() in city["name"].lower()]

    if country:
        filtered_cities = [city for city in filtered_cities if city["country"].lower() == country.lower()]

    if min_population:
        filtered_cities = [city for city in filtered_cities if city["population"] >= min_population]

    if max_population:
        filtered_cities = [city for city in filtered_cities if city["population"] <= max_population]

    # Return 404 if no matching results
    if not filtered_cities:
        return jsonify({"error": "No matching city found"}), 404

    # Sorting (Case-Insensitive)
    if sort in ["population", "name", "country"]:
        reverse_order = True if order.lower() == "desc" else False
        if sort == "name":
            filtered_cities = sorted(filtered_cities, key=lambda x: x["name"].lower(), reverse=reverse_order)
        else:
            filtered_cities = sorted(filtered_cities, key=lambda x: x[sort], reverse=reverse_order)
        if sort == "country":
            filtered_cities = sorted(filtered_cities, key=lambda x: x["country"].lower(), reverse=reverse_order)
        else:
            filtered_cities = sorted(filtered_cities, key=lambda x: x[sort], reverse=reverse_order)
        if sort == "population":
            filtered_cities = sorted(filtered_cities, key=lambda x: x["population"].lower(), reverse=reverse_order)
        else:
            filtered_cities = sorted(filtered_cities, key=lambda x: x[sort], reverse=reverse_order)


    # Return only 5 results
    return jsonify(filtered_cities[:5])




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






#sample dogs_getapi

dogs = [
    {"id": 1, "name": "Ramu", "breed": "Labrador"},
    {"id": 2, "name": "Somu", "breed": "Beagle"},
    {"id": 3, "name": "Raju", "breed": "Golden Retriever"},
    {"id": 4, "name": "Jiju", "breed": "Bulldog"},
    {"id": 5, "name": "Siju", "breed": "Golden Retriever"}
]

@app.route('/dogs', methods=['GET'])
def get_dogs():
    id_param = request.args.get('id')  # Get 'id' query parameter
    name_search = request.args.get('name','').lower()  # Partial name search
    breed_search = request.args.get('breed', '').lower()
    sort_order = request.args.get("sort") # Sorting 
    

    # Check if 'id' is provided and valid
    if id_param:
        if id_param.isdigit():
         filtered_dogs = [dog for dog in dogs if dog['id'] == int(id_param)]
         if not filtered_dogs:  # If no matching dog is found
            return jsonify({"error": f"No dog found with ID {id_param}."}), 404
        else:
            return jsonify({"error": "ID must be an integer."}), 400
    else:
         # Filtering by name or breed if provided
        filtered_dogs = [dog for dog in dogs if 
                         (name_search in dog['name'].lower() if name_search else True) and
                         (breed_search in dog['breed'].lower() if breed_search else True)]
       
         # If no matching dogs are found, return a 404 error instead of an empty list
        if not filtered_dogs:
             return jsonify({"error": f"No dogs found for the given filters"}), 404
   

   # Sorting logic
        if sort_order:
            if sort_order not in ["asc", "desc"]:
                return jsonify({"error": "Invalid sort order. Use 'asc' or 'desc'."}), 400

            def sort_by_name(dogs):
                return dogs["name"]

            filtered_dogs.sort(key=sort_by_name, reverse=(sort_order == "desc"))
            
    return jsonify(filtered_dogs)

@app.route('/dogs/<int:id>', methods=['GET'])
def get_dog_by_id(id: int):
    dog = next((d for d in dogs if d['id'] == id), None)
    return jsonify(dog) if dog else (jsonify({'error': 'Dog not found.'}), 404)



# phone API

phones = [
    {"id": 1, "name": "iPhone 13", "brand": "Apple", "price": 99999},
    {"id": 2, "name": "Samsung Galaxy S21", "brand": "Samsung", "price": 11799},
    {"id": 3, "name": "OnePlus 9", "brand": "OnePlus", "price": 21729},
    {"id": 4, "name": "Google Pixel 6", "brand": "Google", "price": 25599},
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
    # Listen on all network interfaces on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
