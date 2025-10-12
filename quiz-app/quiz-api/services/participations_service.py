from db import SessionLocal
from models import Participations
from datetime import datetime

def add_participation(playerName, score, answers, idVersions):
    session = SessionLocal()
    participation = Participations(
        playerName=playerName,
        score=score,
        date=datetime.utcnow(),
        answers=answers,
        idVersions=idVersions
    )
    session.add(participation)
    session.commit()
    session.close()
    return participation