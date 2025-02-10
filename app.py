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

if __name__ == '__main__':
    # Listen on all network interfaces on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
