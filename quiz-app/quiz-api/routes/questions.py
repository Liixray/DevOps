from flask import Blueprint
from services.questions_service import get_question_by_position, count_questions

questions_bp = Blueprint("questions", __name__, url_prefix="/api/questions")

@questions_bp.route("/quiz", methods=["GET"])
def quiz_question():
    return get_question_by_position()

@questions_bp.route("/count", methods=["GET"])
def quiz_count():
    return count_questions()

