from flask import Blueprint, request, jsonify
from services.questions import get_question_by_position, count_questions, create_question, update_question, delete_question, delete_all_questions
from services.auth_service import admin_required

questions_bp = Blueprint("questions", __name__, url_prefix="/questions")

@questions_bp.route("/quiz", methods=["GET"])
def quiz_question():
    return get_question_by_position()

@questions_bp.route("/count", methods=["GET"])
def quiz_count():
    return count_questions()

@questions_bp.route("/", methods=["POST"])
@admin_required
def create_question_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    return create_question(data)

@questions_bp.route("/<int:question_id>", methods=["PUT"])
@admin_required
def update_question_route(question_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    return update_question(question_id, data)

@questions_bp.route("/<int:question_id>", methods=["DELETE"])
@admin_required
def delete_question_route(question_id):
    return delete_question(question_id)

@questions_bp.route("/all", methods=["DELETE"])
@admin_required
def delete_all_questions_route():
    return delete_all_questions()