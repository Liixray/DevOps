import hashlib
from flask import jsonify
from jwt_utils import build_token

# md5("admin") = 21232f297a57a5a743894a0e4a801fc3
ADMIN_HASH_MD5 = "21232f297a57a5a743894a0e4a801fc3"


def handle_admin_login(payload):
    """
    Traite le login admin:
    - 200 {token} si OK, 400 si input invalide, 401 si accès non autorisé
    """

    password = str(payload.get("password") or "")
    if not password:
        return jsonify({"error": "Password required"}), 400

    provided_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
    if provided_hash != ADMIN_HASH_MD5:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        token = build_token("quiz-app-admin")
        return jsonify({"token": token}), 200
    except Exception:
        return jsonify({"error": "Internal server error"}), 500