# TaskSum — AI To-Do Summarizer

Complete your tasks, then get a one-paragraph AI-generated summary of
what you got done today.

<!-- Add a screenshot or demo GIF here before submitting -->
![demo](docs/demo.gif)

## Features
- Add and list tasks
- Mark tasks complete
- Generate a one-paragraph summary of completed tasks via Gemini

## Tech Stack
FastAPI · Streamlit · google-genai · Pydantic · python-dotenv

## Setup

1. Clone the repo and enter the folder:
   ```bash
   git clone <your-repo-url>
   cd todo-ai-summary
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   ```bash
   cp .env.example .env
   # then edit .env and add your GOOGLE_API_KEY
   ```

4. Run the backend (from the project root):
   ```bash
   uvicorn backend.main:app --reload
   ```

5. In a second terminal, run the frontend:
   ```bash
   streamlit run frontend/app.py
   ```

6. Open the Streamlit URL printed in the terminal (usually
   http://localhost:8501).

## Team
| Role | Member |
|---|---|
| Product & Prompt Lead | _name_ |
| Backend & AI Engineer | _name_ |
| Frontend & UX Lead | _name_ |
| QA & Git Lead | _name_ |
