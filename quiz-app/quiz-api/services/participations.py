from db import SessionLocal
from models import *
from flask import jsonify

def delete_all_participations():
    session = SessionLocal()
    session.query(Participations).delete()
    session.commit()
    session.close()
    return jsonify({"message": "All participations deleted successfully"}), 204