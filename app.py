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



if __name__ == '__main__':
    # Listen on all network interfaces on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
