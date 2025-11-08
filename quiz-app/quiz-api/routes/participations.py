from flask import Blueprint, request, jsonify, current_app
from services.auth_service import admin_required
from services.participations_service import delete_all_participations, add_participation, get_leaderboard_data

participations_bp = Blueprint("participations", __name__, url_prefix="/participations")

@participations_bp.route("/all", methods=["DELETE"])
@admin_required
def delete_participations():
    return delete_all_participations()

@participations_bp.route("", methods=["POST"])
def create_participation():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    playerName = data.get("playerName")
    answers = data.get("answers")
    score = data.get("score", None)
    idVersions = data.get("idVersions", None)

    if not playerName:
        return jsonify({"error": "Missing playerName"}), 400
    if answers is None:
        return jsonify({"error": "Missing answers (expect list of answer ids)"}), 400

    try:
        participation = add_participation(
            playerName=playerName,
            answers=answers,
            idVersions=idVersions,
            score=score
        )
        return jsonify({"message": "Participation enregistrée", "id": getattr(participation, "id", None)}), 201
    except Exception as e:
        current_app.logger.exception("create_participation failed: %s", e)
        return jsonify({"error": str(e)}), 500
    
@participations_bp.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    page = request.args.get("page", type=int, default=1)
    limit = request.args.get("limit", type=int, default=20)
    try:
        leaderboard = get_leaderboard_data(page=page, limit=limit)
        return jsonify(leaderboard), 200
    except Exception as e:
        current_app.logger.exception("get_leaderboard failed: %s", e)
        return jsonify({"error": str(e)}), 500