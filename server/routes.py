from flask import Blueprint, jsonify, request
from server.models import Plant
from server.config import db

plants_bp = Blueprint('plants', __name__)

# GET /plants/:id
@plants_bp.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = db.session.get(Plant, id)
    if not plant:
        return {"error": "Plant not found"}, 404
    return jsonify(plant.to_dict()), 200

# PATCH /plants/:id
@plants_bp.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = db.session.get(Plant, id)
    if not plant:
        return {"error": "Plant not found"}, 404

    data = request.get_json()
    if "is_in_stock" in data:
        plant.is_in_stock = data["is_in_stock"]
        db.session.commit()

    return jsonify(plant.to_dict()), 200

# DELETE /plants/:id
@plants_bp.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = db.session.get(Plant, id)
    if not plant:
        return {"error": "Plant not found"}, 404

    db.session.delete(plant)
    db.session.commit()
    return '', 204
