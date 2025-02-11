import json
from flask import Flask, jsonify, request
app = Flask(__name__)

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





if __name__ == '__main__':
   app.run(port=5000)