# SPEC.md — TaskSum (AI To-Do Summarizer)

## Problem Statement
Who is the user: someone managing a daily to-do list who finishes several
small tasks and wants a quick sense of what they actually accomplished,
without re-reading the whole list.
Friction solved: raw checked-off task lists don't tell a story — the user
has to mentally summarize their own day. TaskSum turns completed tasks
into a one-paragraph human-readable summary on demand.

## MVP Scope (strictly 3 features — nothing else)
1. **Add & list tasks** — user can add a task (text) and see all tasks
   with their status (pending / complete).
2. **Mark task complete** — user can toggle a task to complete.
3. **Generate summary** — user clicks "Summarize" and the backend sends
   all completed tasks to an LLM, which returns one paragraph describing
   the day's progress.

Explicitly OUT of scope: due dates, priorities, categories, multi-user
accounts, persistence beyond in-memory (no DB), editing/deleting tasks.

## Tech Stack
- Backend: `fastapi`, `uvicorn`
- Validation: `pydantic`
- LLM: `google-genai`
- Frontend: `streamlit`, `requests`
- Env management: `python-dotenv`
- Storage: in-memory Python list (no DB — out of scope for 60 min)

## Environment Setup
`.env.example` defines:
```
GOOGLE_API_KEY=your_key_here
```
Each teammate copies `.env.example` → `.env` and fills in their own key.
`.env` is git-ignored — never committed.

## API Contract (backend/main.py)
- `POST /tasks` — body: `{ "title": str }` → returns created task
- `GET /tasks` — returns list of all tasks
- `PATCH /tasks/{task_id}/complete` — marks a task complete
- `POST /summary` — no body → returns `{ "summary": str }` generated
  from all currently-completed tasks

## Team Roles (this build)
- Product & Prompt Lead: owns this SPEC.md, keeps scope to 3 features
- Backend & AI Engineer: `backend/main.py`, `backend/models.py`, `backend/llm.py`
- Frontend & UX Lead: `frontend/app.py`
- QA & Git Lead: repo setup, `.gitignore`, testing edge cases, README, commits
