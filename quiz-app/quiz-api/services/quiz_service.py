from db import SessionLocal
from models import Questions, Participations

def get_quiz_info():
    session = SessionLocal()
    try:
        # Les questions
        questions = session.query(Questions).all()
        size = len(questions)

        # Participations
        participations = session.query(Participations).all()
        scores = [
            {
                "playerName": p.playerName,
                "score": p.score,
                "date": p.date.isoformat() if p.date else None
            }
            for p in participations
        ]

        return {
            "size": size,
            "scores": scores
        }
    except Exception as e:
        return {
            "error": str(e)
        }
    finally:
        session.close()