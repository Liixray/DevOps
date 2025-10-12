from flask import jsonify
from sqlalchemy import select
from db import SessionLocal
from models import Users
from jwt_utils import build_token
from werkzeug.security import generate_password_hash, check_password_hash

HASH_METHOD = "scrypt" 


def register_user(payload):
    """
    Crée un utilisateur (name, mail, password).
    Réponses:
      - 201 {id, name, mail}
      - 400 champs manquants
      - 409 mail déjà utilisé
    """
    name = str(payload.get("name") or "").strip()
    mail = str(payload.get("mail") or "").strip().lower()
    password = str(payload.get("password") or "")

    if not name:
        return jsonify({"error": "Name required"}), 400
    if not mail:
        return jsonify({"error": "Email required"}), 400
    if not password:
        return jsonify({"error": "Password required"}), 400

    try:
        with SessionLocal() as session:
            exists = session.execute(select(Users).where(Users.mail == mail)).scalar_one_or_none()
            if exists:
                return jsonify({"error": "Email already in use"}), 409

            user = Users(
                name=name,
                mail=mail,
                password=generate_password_hash(password, method=HASH_METHOD),
            )
            session.add(user)
            session.commit()
            return jsonify({"id": user.id, "name": user.name, "mail": user.mail}), 201
    except Exception:
        return jsonify({"error": "Internal server error"}), 500


def handle_user_login(payload):
    """
    Login utilisateur via email + password.
      - 200 {token}
      - 400 champs manquants
      - 401 identifiants invalides
    """
    mail = str(payload.get("mail") or "").strip().lower()
    password = str(payload.get("password") or "")

    if not mail:
        return jsonify({"error": "Email required"}), 400
    if not password:
        return jsonify({"error": "Password required"}), 400

    try:
        with SessionLocal() as session:
            user = session.execute(select(Users).where(Users.mail == mail)).scalar_one_or_none()
            if not user or not check_password_hash(user.password, password):
                return jsonify({"error": "Unauthorized"}), 401

            token = build_token(f"user:{user.id}")
            return jsonify({"token": token}), 200
    except Exception:
        return jsonify({"error": "Internal server error"}), 500