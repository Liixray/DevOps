from models import Base, Questions, Versions, Answers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

db_user = os.environ.get("DATABASE_USER", "")
db_pass = os.environ.get("DATABASE_PASSWORD", "")
db_host = os.environ.get("DATABASE_HOST", "localhost")
db_port = os.environ.get("DATABASE_PORT", "3306")
db_name = os.environ.get("DATABASE_NAME", "")

if db_user and db_pass and db_name:
    DATABASE_URL = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    Base.metadata.create_all(engine)

def seed_questions():
    session = SessionLocal()
    # Créer une version pour lier les questions
    version = Versions(date=datetime.utcnow())
    session.add(version)
    session.commit()  # Pour obtenir l'id de la version

    questions_data = [
        {
            "position": 1,
            "title": "Quelle est la capitale de la France ?",
            "text": "Choisissez la bonne réponse.",
            "answers": [
                {"text": "Paris", "isCorrect": True},
                {"text": "Lyon", "isCorrect": False},
                {"text": "Marseille", "isCorrect": False},
                {"text": "Toulouse", "isCorrect": False},
            ]
        },
        {
            "position": 2,
            "title": "Combien font 2 + 2 ?",
            "text": "Addition simple.",
            "answers": [
                {"text": "3", "isCorrect": False},
                {"text": "4", "isCorrect": True},
                {"text": "5", "isCorrect": False},
                {"text": "22", "isCorrect": False},
            ]
        },
        {
            "position": 3,
            "title": "Quel est le plus grand océan du monde ?",
            "text": None,
            "answers": [
                {"text": "Océan Atlantique", "isCorrect": False},
                {"text": "Océan Indien", "isCorrect": False},
                {"text": "Océan Pacifique", "isCorrect": True},
                {"text": "Océan Arctique", "isCorrect": False},
            ]
        },
    ]

    for q in questions_data:
        question = Questions(
            position=q["position"],
            title=q["title"],
            text=q["text"],
            image=None,
            idVersions=version.id
        )
        session.add(question)
        session.flush()  # Pour obtenir l'id de la question

        answers = [
            Answers(
                idQuestions=question.id,
                text=ans["text"],
                isCorrect=ans["isCorrect"]
            ) for ans in q["answers"]
        ]
        session.add_all(answers)

    session.commit()
    session.close()

if __name__ == "__main__":
    init_db()
    seed_questions()