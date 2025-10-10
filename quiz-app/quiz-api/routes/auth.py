from flask import Blueprint, request, jsonify, current_app
from services.auth_service import handle_admin_login

auth_bp = Blueprint('auth', __name__, url_prefix="/api/auth/admin")

@auth_bp.route('/login', methods=['POST'])
def admin_login():

    payload = request.get_json()
    if payload is None:
        return jsonify({"error": "Invalid JSON body"}), 400

    try:
        return handle_admin_login(payload)
    except Exception as exc:
        current_app.logger.exception("auth.login failed: %s", exc)
        return jsonify({"error": "Internal server error"}), 500
