from flask import Blueprint, request, jsonify

import sys
from pathlib import Path
PARENT = Path(__file__).resolve().parents[2]
if str(PARENT) not in sys.path:
    sys.path.append(str(PARENT))

from jwt_utils import build_token

auth_bp = Blueprint('auth', __name__, url_prefix="/api/auth")

# md5("admin") = 21232f297a57a5a743894a0e4a801fc3
ADMIN_HASH_MD5 = "21232f297a57a5a743894a0e4a801fc3"

@auth_bp.route('/login', methods=['POST'])
def admin_login():
    payload = request.get_json(silent=True) or {}
    password = payload.get('password', '')

    import hashlib
    provided_hash = hashlib.md5(password.encode('utf-8')).hexdigest()

    if provided_hash != ADMIN_HASH_MD5:
        return 'Unauthorized', 401

    token = build_token()
    return jsonify({"token": token}), 200
