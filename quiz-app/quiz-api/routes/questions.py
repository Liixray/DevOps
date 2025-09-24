from flask import Blueprint

questions_bp = Blueprint("questions", __name__, url_prefix="/api/questions")