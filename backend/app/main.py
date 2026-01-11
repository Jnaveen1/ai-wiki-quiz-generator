from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from urllib.parse import urlparse
import json
from fastapi.middleware.cors import CORSMiddleware
import os 

from app.database import engine, get_db
from app.models import Base, Article, Quiz
from app.scraper import scrape_wikipedia
from app.llm import generate_quiz_from_text

# ----------------------------
# App init
# ----------------------------
app = FastAPI(title="AI Wiki Quiz Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# ----------------------------
# Utility functions
# ----------------------------
def validate_url(url: str):
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise HTTPException(status_code=400, detail="Invalid URL")


def get_or_create_article(db: Session, url: str, title: str, summary: str):
    article = db.query(Article).filter(Article.url == url).first()
    if article:
        return article

    article = Article(
        url=url,
        title=title,
        summary=summary
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def save_quiz(db: Session, article_id: int, q: dict):
    quiz = Quiz(
        article_id=article_id,
        question=q["question"],
        options=json.dumps(q["options"]),
        answer=q["answer"],
        difficulty=q.get("difficulty"),
        explanation=q.get("explanation")
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz

def parse_options(raw):
    # already list (future-proof)
    if isinstance(raw, list):
        return raw

    # try JSON
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return parsed
    except Exception:
        pass

    # fallback: split string
    return [opt.strip() for opt in raw.split(",") if opt.strip()]

# ----------------------------
# Routes
# ----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/scrape-test")
def scrape_test():
    return scrape_wikipedia("https://en.wikipedia.org/wiki/Alan_Turing")


@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    existing = db.query(Article).filter(Article.url == "test-url").first()

    if not existing:
        article = Article(
            url="test-url",
            title="Test Title",
            summary=None
        )
        db.add(article)
        db.commit()

    return {"status": "DB connected and working"}


@app.get("/llm-test")
def llm_test():
    scraped = scrape_wikipedia("https://en.wikipedia.org/wiki/Alan_Turing")
    raw_output = generate_quiz_from_text(scraped["content"])

    # IMPORTANT: LLM returns string → convert to dict
    return json.loads(raw_output)


@app.get("/generate-quiz")
def generate_quiz(url: str, db: Session = Depends(get_db)):
    validate_url(url)

    # 1. Scrape
    scraped = scrape_wikipedia(url)

    # 2. Article (idempotent)
    article = get_or_create_article(
        db=db,
        url=url,
        title=scraped["title"],
        summary=scraped["summary"]
    )

    # 3. If quizzes already exist → return early
    existing_count = db.query(Quiz).filter(Quiz.article_id == article.id).count()
    if existing_count > 0:
        return {
            "article_id": article.id,
            "quiz_count": existing_count,
            "status": "already generated"
        }

    # 4. Generate quiz (LLM safety)
    try:
        raw_output = generate_quiz_from_text(scraped["content"])
        quiz_data = json.loads(raw_output)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Quiz generation failed"
        )

    # 5. Save quizzes
    saved = []
    for q in quiz_data["quiz"]:
        saved.append(save_quiz(db, article.id, q))

    return {
        "article_id": article.id,
        "quiz_count": len(saved),
        "status": "saved successfully"
    }

@app.get("/articles")
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).all()
    return [
        {
            "id": a.id,
            "url": a.url,
            "title": a.title,
            "summary": a.summary
        }
        for a in articles
    ]

@app.get("/articles/{article_id}/quizzes")
def get_quizzes(article_id: int, db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).filter(Quiz.article_id == article_id).all()

    return [
        {
            "question": q.question,
            "options": parse_options(q.options),  # 🔥 FIX HERE
            "answer": q.answer,
            "difficulty": q.difficulty,
            "explanation": q.explanation
        }
        for q in quizzes
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )