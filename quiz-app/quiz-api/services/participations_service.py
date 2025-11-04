from db import SessionLocal
from models import Participations, Answers
from datetime import datetime
from flask import jsonify

def delete_all_participations():
    session = SessionLocal()
    session.query(Participations).delete()
    session.commit()
    session.close()
    return jsonify({"message": "All participations deleted successfully"}), 204

def add_participation(playerName, answers, idVersions=None, score=None):
    """
    Persist a participation.
    - answers: list of answer IDs (or None). We compute the score if score is None.
    - idVersions: optional version id
    - returns the created Participations instance
    """
    session = SessionLocal()
    try:
        # normalize answers list
        if answers is None:
            answers_list = []
        else:
            # ensure it's a list
            answers_list = list(answers)

        # compute score if not provided: each answer id -> check Answers.isCorrect
        computed_score = 0
        for aid in answers_list:
            try:
                if aid is None:
                    continue
                ans = session.get(Answers, int(aid))
                if ans and getattr(ans, "isCorrect", False):
                    computed_score += 1
            except Exception:
                # if an id is invalid, ignore it
                continue

        final_score = score if isinstance(score, int) else computed_score

        participation = Participations(
            playerName=playerName,
            score=final_score,
            date=datetime.utcnow(),
            answers=answers_list,
            idVersions=idVersions if idVersions is not None else 1
        )

        session.add(participation)
        session.commit()
        session.refresh(participation)
        return participation
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()