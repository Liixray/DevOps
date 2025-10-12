from db import SessionLocal
from models import Questions
from flask import request, jsonify
from sqlalchemy.orm import selectinload

def get_question_by_position():
    position = request.args.get("position", type=int)
    if position is None:
        return jsonify({"error": "Missing 'position' parameter"}), 400

    session = SessionLocal()
    question = session.query(Questions)\
        .options(selectinload(Questions.answers))\
        .filter_by(position=position).first()

    if question is None:
        session.close()
        return jsonify({"error": "Question not found"}), 404

    answers = [
        {
            "id": answer.id,
            "text": answer.text,
            "isCorrect": answer.isCorrect
        }
        for answer in question.answers
    ]
    session.close()

    return jsonify({
        "id": question.id,
        "position": question.position,
        "title": question.title,
        "text": question.text,
        "image": question.image,
        "idVersions": question.idVersions,
        "answers": answers
    })

def count_questions():
    session = SessionLocal()
    count = session.query(Questions).count()
    session.close()
    return jsonify({"count": count})