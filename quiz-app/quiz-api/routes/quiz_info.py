from flask import Blueprint, jsonify
from services.quiz_service import get_quiz_info

quiz_info_bp = Blueprint("quiz-info", __name__, url_prefix="/api")

@quiz_info_bp.route("/quiz-info", methods=["GET"])
def quiz_info():
    info = get_quiz_info()
    if "error" in info:
        return jsonify({"error": info["error"]}), 500
    return jsonify(info), 200