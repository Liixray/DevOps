from flask import Blueprint, request, jsonify
from services.auth_service import admin_required

participations_bp = Blueprint("participations", __name__, url_prefix="/participations")

@participations_bp.route("/all", methods=["DELETE"])
@admin_required
def delete_all_participations():
    return delete_all_participations()