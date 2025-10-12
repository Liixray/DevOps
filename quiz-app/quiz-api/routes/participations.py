from flask import Blueprint, request, jsonify
from models import Participations
from services.participations_service import add_participation

participations_bp = Blueprint("participations", __name__, url_prefix="/api/participations")

@participations_bp.route("/add", methods=["POST"])
def create_participation():
    data = request.get_json()
    participation = add_participation(
        playerName=data["playerName"],
        score=data["score"],
        answers=data["answers"],
        idVersions=data["idVersions"]
    )
    return jsonify({"message": "La participation au quiz a été enregistrée", "id": participation.id}), 201