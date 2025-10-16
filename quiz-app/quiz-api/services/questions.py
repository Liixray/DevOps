from db import SessionLocal
from models import *
from flask import request, jsonify
from sqlalchemy.orm import selectinload
from datetime import datetime

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

def create_question(data):
    required_fields = ["position", "title", "text", "possibleAnswers", "image"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
        
    session = SessionLocal()
    question_count = session.query(Questions).count()
    
    if data["position"] < 1 or data["position"] > question_count + 1:
        session.close()
        return jsonify({"error": "Position must be between 1 and %d" % (question_count + 1)}), 400

    if data["position"] <= question_count:
        session.query(Questions).filter(Questions.position >= data["position"]).update(
            {Questions.position: Questions.position + 1}, synchronize_session=False
        )
    
    latest_version = session.query(Versions).order_by(Versions.id.desc()).first()
    if not latest_version:
        new_version = Versions(date=datetime.utcnow())
        session.add(new_version)
        session.commit()
        id_versions = new_version.id
    else:
        id_versions = latest_version.id

    new_question = Questions(
        position=data["position"],
        title=data["title"],
        text=data.get("text"),
        image=data.get("image"),
        idVersions=id_versions
    )
    session.add(new_question)
    session.commit()

    answer_texts = set()
    correct_count = 0
    for answer_data in data["possibleAnswers"]:
        if "text" not in answer_data or "isCorrect" not in answer_data:
            session.rollback()
            session.close()
            return jsonify({"error": "Each answer must have 'text' and 'isCorrect' fields"}), 400
        if answer_data["text"] in answer_texts:
            session.rollback()
            session.close()
            return jsonify({"error": "Duplicate answer text"}), 400
        answer_texts.add(answer_data["text"])
        if answer_data["isCorrect"]:
            correct_count += 1
        new_answer = Answers(
            idQuestions=new_question.id,
            text=answer_data["text"],
            isCorrect=answer_data["isCorrect"]
        )
        session.add(new_answer)

    if correct_count == 0:
        session.rollback()
        session.close()
        return jsonify({"error": "At least one answer must be correct"}), 400

    session.commit()
    qid = new_question.id
    session.close()

    return jsonify({"id": qid}), 200

def update_question(question_id, data):
    session = SessionLocal()
    question = session.query(Questions).filter_by(id=question_id).first()
    if not question:
        session.close()
        return jsonify({"error": "Question not found"}), 404

    if "position" in data:
        new_position = data["position"]
        question_count = session.query(Questions).count()
        if new_position < 1 or new_position > question_count:
            session.close()
            return jsonify({"error": "Position must be between 1 and %d" % question_count}), 400
        if new_position != question.position:
            if new_position < question.position:
                session.query(Questions).filter(
                    Questions.position >= new_position,
                    Questions.position < question.position
                ).update({Questions.position: Questions.position + 1}, synchronize_session=False)
            else:
                session.query(Questions).filter(
                    Questions.position <= new_position,
                    Questions.position > question.position
                ).update({Questions.position: Questions.position - 1}, synchronize_session=False)
            question.position = new_position

    if "title" in data:
        question.title = data["title"]
    if "text" in data:
        question.text = data["text"]
    if "image" in data:
        question.image = data["image"]

    latest_version = session.query(Versions).order_by(Versions.id.desc()).first()
    if not latest_version:
        new_version = Versions(date=datetime.utcnow())
        session.add(new_version)
        session.commit()
        question.idVersions = new_version.id
    else:
        question.idVersions = latest_version.id

    if "possibleAnswers" in data:
        existing_answers = {ans.id: ans for ans in question.answers}
        answer_texts = set()
        correct_count = 0
        for answer_data in data["possibleAnswers"]:
            if "text" not in answer_data or "isCorrect" not in answer_data:
                session.rollback()
                session.close()
                return jsonify({"error": "Each answer must have 'text' and 'isCorrect' fields"}), 400
            if answer_data["text"] in answer_texts:
                session.rollback()
                session.close()
                return jsonify({"error": "Duplicate answer text"}), 400
            answer_texts.add(answer_data["text"])
            if answer_data["isCorrect"]:
                correct_count += 1

            if "id" in answer_data and answer_data["id"] in existing_answers:
                ans = existing_answers[answer_data["id"]]
                ans.text = answer_data["text"]
                ans.isCorrect = answer_data["isCorrect"]
                del existing_answers[answer_data["id"]]
            else:
                new_answer = Answers(
                    idQuestions=question.id,
                    text=answer_data["text"],
                    isCorrect=answer_data["isCorrect"]
                )
                session.add(new_answer)
        for ans in existing_answers.values():
            session.delete(ans)
        if correct_count == 0:
            session.rollback()
            session.close()
            return jsonify({"error": "At least one answer must be correct"}), 400
    session.commit()
    session.close()
    return jsonify({"message": "Question updated successfully"}), 204

def delete_question(question_id):
    session = SessionLocal()
    question = session.query(Questions).filter_by(id=question_id).first()
    if not question:
        session.close()
        return jsonify({"error": "Question not found"}), 404

    session.query(Answers).filter_by(idQuestions=question_id).delete()

    position = question.position
    session.delete(question)
    session.commit()

    session.query(Questions).filter(Questions.position > position).update(
        {Questions.position: Questions.position - 1}, synchronize_session=False
    )
    session.commit()
    session.close()
    return jsonify({"message": "Question deleted successfully"}), 204

def delete_all_questions():
    session = SessionLocal()
    session.query(Answers).delete()
    session.query(Questions).delete()
    session.commit()
    session.close()
    return jsonify({"message": "All questions deleted successfully"}), 204