from flask import Flask, request, jsonify

app = Flask(__name__)

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


    # if sort_order:
    #     if sort_order not in ["asc", "desc"]:
    #         return jsonify({"error": "Invalid sort order. Use 'asc' or 'desc'."}), 400
    #     filtered_dinosaurs.sort(key=lambda d: d["name"], reverse=(sort_order == "desc"))

    # return jsonify(filtered_dinosaurs)

    # Sorting without using lambda
    # def sort_by_name(dino):
    #     return dino["name"]

    # if sort_order == "asc":
    #     filtered_dinosaurs.sort(key=sort_by_name)
    # elif sort_order == "desc":
    #     filtered_dinosaurs.sort(key=sort_by_name, reverse=True)
    # return jsonify(filtered_dinosaurs)

if __name__ == "__main__":
    app.run()