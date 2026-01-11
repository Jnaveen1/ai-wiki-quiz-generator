import { useEffect, useState } from "react";
import "./App.css";

const API = "https://ai-wiki-quiz-generator-5tab.onrender.com";

function App() {
  const [url, setUrl] = useState("");
  const [articles, setArticles] = useState([]);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadArticles();
  }, []);

  const loadArticles = async () => {
    const res = await fetch(`${API}/articles`);
    const data = await res.json();
    setArticles(data);
  };

const generateQuiz = async () => {
  if (!url) return;
  setLoading(true);

  // 1. Generate quiz
  const res = await fetch(
    `${API}/generate-quiz?url=${encodeURIComponent(url)}`
  );
  const data = await res.json();

  // 2. Load quizzes immediately
  const quizRes = await fetch(
    `${API}/articles/${data.article_id}/quizzes`
  );
  const quizData = await quizRes.json();

  setQuizzes(quizData);

  // 3. Refresh articles & UI
  await loadArticles();
  setSelectedArticle({ id: data.article_id });

  setUrl("");
  setLoading(false);
};


  const loadQuizzes = async (article) => {
    setSelectedArticle(article);
    const res = await fetch(`${API}/articles/${article.id}/quizzes`);
    const data = await res.json();
    setQuizzes(data);
  };

  return (
    <div className="container">
      <h1>AI Wiki Quiz Generator</h1>

      <div className="input-box">
        <input
          placeholder="Paste Wikipedia URL..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button onClick={generateQuiz}>
          {loading ? "Generating..." : "Generate Quiz"}
        </button>
      </div>

      <div className="layout">
        <div className="sidebar">
          <h3>Articles</h3>
          {articles.map((a) => (
            <div
              key={a.id}
              className={`article ${
                selectedArticle?.id === a.id ? "active" : ""
              }`}
              onClick={() => loadQuizzes(a)}
            >
              {a.title}
            </div>
          ))}
        </div>

        <div className="content">
          {quizzes.map((q, idx) => (
            <div className="card" key={idx}>
              <div className={`badge ${q.difficulty}`}>
                {q.difficulty?.toUpperCase()}
              </div>

              <h3>{idx + 1}. {q.question}</h3>

              <ul>
                {q.options.map((opt, i) => (
                  <li key={i}>{opt}</li>
                ))}
              </ul>

              <details>
                <summary>Show Answer</summary>
                <p><strong>Answer:</strong> {q.answer}</p>
                {q.explanation && <p>{q.explanation}</p>}
              </details>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
