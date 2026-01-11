from sqlalchemy.orm import Session
from .models import Article, Quiz
import json

def get_or_create_article(db: Session, url: str, title: str, summary: str):
    article = db.query(Article).filter(Article.url == url).first()
    if article:
        return article

    article = Article(url=url, title=title, summary=summary)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def save_quiz(db: Session, article_id: int, quiz: dict):
    q = Quiz(
        question=quiz["question"],
        options=json.dumps(quiz["options"]),
        answer=quiz["answer"],
        difficulty=quiz.get("difficulty"),
        explanation=quiz.get("explanation"),
        article_id=article_id
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return q

def get_all_articles(db: Session):
    return db.query(Article).all()


def get_quizzes_by_article(db: Session, article_id: int):
    quizzes = db.query(Quiz).filter(Quiz.article_id == article_id).all()

    return [
        {
            "id": q.id,
            "question": q.question,
            "options": json.loads(q.options),
            "answer": q.answer,
            "difficulty": q.difficulty,
            "explanation": q.explanation
        }
        for q in quizzes
    ]