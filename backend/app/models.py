from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text)

    quizzes = relationship("Quiz", back_populates="article", cascade="all, delete")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    options = Column(Text, nullable=False)   # stored as JSON string
    answer = Column(String, nullable=False)
    difficulty = Column(String)
    explanation = Column(Text)

    article_id = Column(Integer, ForeignKey("articles.id"))
    article = relationship("Article", back_populates="quizzes")
