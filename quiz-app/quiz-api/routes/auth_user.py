from flask import Blueprint, request, jsonify, current_app
from services.auth_user_service import handle_user_login, register_user

auth_user_bp = Blueprint('auth_user', __name__, url_prefix="/api/auth/user")

@auth_user_bp.route('/register', methods=['POST'])
def user_register():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Invalid JSON body"}), 400
    try:
        return register_user(payload)
    except Exception as exc:
        current_app.logger.exception("auth_user.user_register failed: %s", exc)
        return jsonify({"error": "Internal server error"}), 500

@auth_user_bp.route('/login', methods=['POST'])
def user_login():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Invalid JSON body"}), 400
    try:
        return handle_user_login(payload)
    except Exception as exc:
        current_app.logger.exception("auth_user.user_login failed: %s", exc)
        return jsonify({"error": "Internal server error"}), 500