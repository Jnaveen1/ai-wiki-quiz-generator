import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-flash-latest"  # confirmed available in your account


def generate_quiz_from_text(article_text: str):
    # Safety cap
    article_text = article_text[:12000]

    prompt = f"""
You are an API that returns ONLY valid JSON.

Using ONLY the article content below, generate a quiz.

RULES:
- 5 to 10 questions
- Each question has exactly 4 options
- Exactly ONE correct answer
- Difficulty must be: easy | medium | hard
- Explanation must be grounded in the article
- NO markdown
- NO extra text
- NO hallucinations

OUTPUT FORMAT:
{{
  "quiz": [
    {{
      "question": "",
      "options": ["", "", "", ""],
      "answer": "",
      "difficulty": "",
      "explanation": ""
    }}
  ],
  "related_topics": ["", "", ""]
}}

ARTICLE CONTENT:
{article_text}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "temperature": 0.2,
            "response_mime_type": "application/json",
        },
    )

    return response.text
