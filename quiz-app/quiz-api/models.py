from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey, Boolean, JSON, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Versions(Base):
    __tablename__ = "versions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    questions: Mapped[list["Questions"]] = relationship(back_populates="versions", cascade="all, delete-orphan")
    participations: Mapped[list["Participations"]] = relationship(back_populates="versions", cascade="all, delete-orphan")

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    mail: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

class Questions(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    image: Mapped[str | None] = mapped_column(String(255), nullable=True)
    idVersions: Mapped[int] = mapped_column(ForeignKey("versions.id"), nullable=False)
    versions: Mapped["Versions"] = relationship(back_populates="questions")
    answers: Mapped[list["Answers"]] = relationship(back_populates="questions", cascade="all, delete-orphan")

class Answers(Base):
    __tablename__ = "answers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    idQuestions: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    isCorrect: Mapped[bool] = mapped_column(Boolean, default=False)
    questions: Mapped["Questions"] = relationship(back_populates="answers")

class Participations(Base):
    __tablename__ = "participations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    playerName: Mapped[str] = mapped_column(String(255), nullable=False)
    score: Mapped[int] = mapped_column(Integer, default=0)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    answers: Mapped[list[int] | None] = mapped_column(JSON, nullable=True)
    idVersions: Mapped[int] = mapped_column(ForeignKey("versions.id"), nullable=False)
    versions: Mapped["Versions"] = relationship(back_populates="participations")
