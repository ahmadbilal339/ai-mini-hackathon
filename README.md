# TaskSum

TaskSum is a lightweight AI-powered task management application. It allows users to add and complete daily tasks, then generates a concise one-paragraph summary of their completed work.

This project was developed collaboratively during the **Group AI Mini Hackathon** using a specification-first and incremental development approach.

## MVP Features

- Add daily tasks through a simple web interface.
- View and track task completion.
- Generate an AI-powered summary of completed tasks.
- Display user-friendly messages when the backend or AI service is unavailable.

## Tech Stack

| Area | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| Validation | Pydantic |
| AI Integration | Google Gemini (`google-genai`) |
| API Communication | Requests |
| Environment Management | `python-dotenv` |
| Language | Python |

## Project Structure

```text
ai-mini-hackathon/
├── backend/
│   ├── llm.py
│   ├── main.py
│   └── models.py
├── frontend/
│   └── app.py
├── assets/
│   └── demo.png
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── SPEC.md
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/ahmadbilal339/ai-mini-hackathon.git
cd ai-mini-hackathon
```

### 2. Create a virtual environment

```bash
python -m venv myenv
```

Activate it on Windows CMD:

```bat
myenv\Scripts\activate
```

Activate it on Windows PowerShell:

```powershell
.\myenv\Scripts\Activate.ps1
```

Activate it on macOS/Linux:

```bash
source myenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file from `.env.example`.

Windows CMD:

```bat
copy .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Open `.env` and provide the required Google Gemini API key using the variable name defined in `.env.example`. Never commit the `.env` file.

## Run the Application

### 1. Start the FastAPI backend

```bash
uvicorn backend.main:app --reload
```

The backend will run at:

```text
http://localhost:8000
```

Interactive API documentation is available at:

```text
http://localhost:8000/docs
```

### 2. Start the Streamlit frontend

Open a second terminal, activate the virtual environment, and run:

```bash
streamlit run frontend/app.py
```

The frontend will normally open at:

```text
http://localhost:8501
```

Keep both terminals running while using the application.

## How to Use

1. Start the backend and frontend.
2. Enter a task and select **Add**.
3. Mark tasks as completed.
4. Select **Summarize completed tasks** to generate the daily summary.

## Demo

![TaskSum application demo](assets/demo.png)

## QA Checks Performed

- Python syntax compilation completed successfully for the backend and frontend.
- FastAPI health endpoint returned a healthy response.
- Streamlit frontend started successfully.
- Frontend displayed an error message when the backend was stopped.
- `.env` was confirmed as ignored by Git.
- Python virtual environments, cache files, IDE files, logs, and secrets are excluded through `.gitignore`.

## Team Members

| Name | Role | GitHub |
|---|---|---|
| Muhammad Iqbal Shahzad | Product & Prompt Lead | [@Iqbalshahzad96](https://github.com/Iqbalshahzad96) |
| Jazib Faisal | Backend & AI Engineer | [@jazibfaisal4](https://github.com/jazibfaisal4) |
| Ammaduddin Ahmad | Frontend & UX Lead | [@amaduddinahmad1](https://github.com/amaduddinahmad1) |
| Ahmad Bilal | QA & Git Lead | [@ahmadbilal339](https://github.com/ahmadbilal339) |

## Repository

[GitHub Repository](https://github.com/ahmadbilal339/ai-mini-hackathon)
