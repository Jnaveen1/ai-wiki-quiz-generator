const BASE_URL = "http://127.0.0.1:8000"; // change later to deployed backend

export async function generateQuiz(url) {
  const res = await fetch(
    `${BASE_URL}/generate-quiz?url=${encodeURIComponent(url)}`
  );
  return res.json();
}

export async function getArticles() {
  const res = await fetch(`${BASE_URL}/articles`);
  return res.json();
}

export async function getQuizzes(articleId) {
  const res = await fetch(`${BASE_URL}/articles/${articleId}/quizzes`);
  return res.json();
}
