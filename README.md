AI Wiki Quiz Generator: 

  This project is a full-stack web application that generates multiple-choice quizzes from Wikipedia articles.
  A user provides a Wikipedia URL, and the system automatically extracts the content, generates quiz questions using an AI model, and stores everything in a database for later access.
  
  The application is built with a clear separation between frontend, backend, and database, and is fully deployed.

Live Application

  Frontend:
  
    https://ai-wiki-quiz-generator-orpin.vercel.app
    
  Backend:
  
    https://ai-wiki-quiz-generator-5tab.onrender.com

What the Application Does: 

  User pastes a Wikipedia article URL
  
  Backend scrapes the article content
  
  AI model generates quiz questions with:
  
  Multiple options
  
  Correct answer
  
  Difficulty level (easy / medium / hard)
  
  Explanation (if available)
  
  Data is stored in a PostgreSQL database

User can:

  View all generated articles
  
  Click an article to view its quizzes
  
  See difficulty levels and answers

Tech Stack

  Frontend
  
     -  React
     - JavaScript
     -  CSS
     - Deployed on Vercel
     
  Backend
  
    - FastAPI (Python)
    - SQLAlchemy ORM
    - Google Gemini API
    - Deployed on Render
    - Database
    - PostgreSQL (Render managed database)

Project Structure

      ai-wiki-quiz-generator/
      │
      ├── backend/
      │   ├── app/
      │   │   ├── main.py
      │   │   ├── database.py
      │   │   ├── models.py
      │   │   ├── scraper.py
      │   │   └── llm.py
      │   └── requirements.txt
      │
      ├── frontend/
      │   ├── src/
      │   │   └── App.js
      │   └── package.json
      │
      └── README.md


  Backend API Endpoints

  Method	           Endpoint	                   Description
  
  GET	              /health	                    - for  Health check
  
  GET	              /generate-quiz?url=          - is used to Generate quiz from Wikipedia URL

  GET	              /articles	                   - to Get all articles
  
  GET	              /articles/{id}/quizzes	     - is used to Get quizzes for a specific article


Environment Variables (Backend)

  The backend uses the following environment variables:
      DATABASE_URL=postgresql://...
      GEMINI_API_KEY=your_api_key
      
  These are configured in Render for deployment.

Running the Project Locally

  Backend
    cd backend
    python -m venv venv
    source venv/bin/activate   # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload
    
  Frontend
    cd frontend
    npm install
    npm start

Deployment

  Backend: Render Web Service
  
  Database: Render PostgreSQL
  
  Frontend: Vercel
  
Frontend communicates with backend using REST APIs and handles CORS properly.

Assignment Compliance : 

    This project satisfies the assignment requirements
    
    Full-stack implementation
    
    Backend developed first
    
    Database integration
    
    AI-based content generation
    
    Clean API design
    
    Deployed frontend and backend
    
    Proper error handling and validation

Author: 

  Naveen Janapati
