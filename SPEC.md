# AI Study Notes Generator — Project Specification

## 1. Problem Statement

Students often struggle to distill large amounts of study material into concise, actionable notes. Manually summarizing topics, extracting key points, and creating practice questions is time-consuming and inconsistent.

The **AI Study Notes Generator** is a small web application that accepts a topic or study material from the user and uses Google Gemini to automatically produce:

1. A concise summary
2. Important key points
3. 3–5 quiz questions

This MVP demonstrates AI-assisted study preparation within a one-hour hackathon scope.

---

## 2. Target User

- **Primary user:** Students (high school, university, or self-learners) who need quick study notes and quiz questions from a topic or pasted study material.
- **Context:** Single-user, session-based use — no accounts or saved history.

---

## 3. Problem / Friction

| Friction | Description |
|----------|-------------|
| Time cost | Writing summaries and key points by hand takes significant effort. |
| Inconsistency | Self-made notes vary in quality and completeness. |
| No instant practice | Creating quiz questions requires extra cognitive load after reading material. |
| Tool overload | Full-featured note apps add complexity (auth, storage, uploads) beyond what is needed for a quick study session. |

---

## 4. MVP Scope

### Feature 1 — User Input
Allow the user to enter a **topic** or **study material** (plain text) via the Streamlit frontend.

### Feature 2 — Summary & Key Points
Call the FastAPI backend, which uses Google Gemini to generate:
- A **concise summary** of the input
- A list of **important key points**

### Feature 3 — Quiz Questions
Generate **3–5 quiz questions** (with answers or answer hints as appropriate for display) based on the same input.

### Technical MVP Deliverables
- FastAPI backend with a single generation endpoint
- Streamlit frontend that submits input and displays results
- Environment-based configuration for the Gemini API key
- Basic input validation and error handling

---

## 5. Explicitly Out of Scope

The following must **not** be implemented in this MVP:

- Authentication
- User accounts
- Database
- Saved history
- PDF uploads
- File uploads
- Admin dashboard
- Analytics
- Multiple users / multi-tenancy
- Computer vision
- Voice features
- Chat history
- Any feature not explicitly listed in **MVP Scope**

---

## 6. Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, FastAPI, Pydantic |
| Frontend | Streamlit |
| AI | Google Gemini API (`google-genai`) |
| Environment | `python-dotenv` |
| HTTP (client) | `requests` |
| ASGI server | `uvicorn` |
| Version control | Git, GitHub |

---

## 7. Application Architecture

```
┌─────────────────┐      HTTP POST       ┌─────────────────┐      API call      ┌─────────────────┐
│  Streamlit      │  ─────────────────►  │  FastAPI        │  ───────────────►  │  Google Gemini  │
│  (frontend/)    │  /generate-notes     │  (backend/)     │                    │  API            │
│                 │  ◄─────────────────  │                 │  ◄───────────────  │                 │
└─────────────────┘      JSON response   └─────────────────┘      text/JSON     └─────────────────┘
```

### Components

1. **Frontend (`frontend/`)** — Streamlit app: text input, submit button, display summary, key points, and quiz questions.
2. **Backend (`backend/`)** — FastAPI app: validates request, builds prompt, calls Gemini, returns structured JSON.
3. **Configuration** — `GEMINI_API_KEY` loaded from `.env` via `python-dotenv` (never committed).

### Data Flow

1. User enters topic or study material in Streamlit.
2. Frontend sends `POST /generate-notes` with JSON body `{ "topic_or_material": "<text>" }`.
3. Backend validates input, calls Gemini with a structured prompt.
4. Backend parses/normalizes Gemini output into `{ summary, key_points, quiz_questions }`.
5. Frontend renders the response.

No persistence layer. Each request is stateless.

---

## 8. API Specification

### `POST /generate-notes`

Generate study notes from user-provided text.

**Request**

```json
{
  "topic_or_material": "string (required)"
}
```

**Success Response — `200 OK`**

```json
{
  "summary": "string",
  "key_points": ["string", "..."],
  "quiz_questions": [
    {
      "question": "string",
      "answer": "string"
    }
  ]
}
```

**Error Responses**

| Status | Condition | Example body |
|--------|-----------|--------------|
| `422` | Validation failure (empty/missing input, too long) | FastAPI validation detail |
| `500` | Gemini API failure or unexpected server error | `{ "detail": "..." }` |
| `503` | Missing or invalid API key configuration | `{ "detail": "..." }` |

**Health check (optional, recommended)**

| Method | Path | Response |
|--------|------|----------|
| `GET` | `/health` | `{ "status": "ok" }` |

---

## 9. Validation Requirements

### Request validation
- `topic_or_material` is **required**.
- Must be non-empty after trimming whitespace.
- Maximum length: **10,000 characters** (configurable constant in backend).
- Reject requests that fail validation with `422`.

### Response validation
- Backend must return well-formed JSON matching the success schema.
- `key_points`: non-empty list of strings (when generation succeeds).
- `quiz_questions`: **3–5** items, each with `question` and `answer` strings.

### Frontend validation
- Disable or warn on submit when input is empty.
- Display user-friendly messages for API errors (network, validation, server).

---

## 10. Environment Setup

1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment (OS-specific).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Copy environment template and set your key:
   ```bash
   cp .env.example .env
   ```
   Edit `.env`:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
6. Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).
7. Run backend and frontend in separate terminals (see README.md).

**Never** commit `.env` or real API keys to the repository.

---

## 11. Security Requirements

- Store `GEMINI_API_KEY` only in `.env` (gitignored).
- Provide `.env.example` with a placeholder value only.
- Do not log API keys or full user input in production logs (minimal logging for MVP).
- Validate and bound input length to reduce abuse and cost.
- Backend should not expose internal stack traces to clients in error responses.
- CORS: allow Streamlit origin for local development only (restrict as needed).
- No authentication required for MVP; app is intended for local/demo use.

---

## 12. MVP Success Criteria

The MVP is complete when:

- [ ] User can enter a topic or study material in the Streamlit UI.
- [ ] Clicking generate triggers a call to the FastAPI backend.
- [ ] Backend successfully calls Google Gemini using the configured API key.
- [ ] Response includes a concise **summary**.
- [ ] Response includes a list of **key points**.
- [ ] Response includes **3–5 quiz questions** with answers.
- [ ] Empty or invalid input is rejected with clear feedback.
- [ ] Missing API key produces a clear configuration error (not a silent failure).
- [ ] No out-of-scope features (auth, DB, uploads, history) are present.
- [ ] Project runs locally following README instructions.
- [ ] No secrets are committed to the repository.

---

*This document is the source of truth for MVP scope. Do not implement features outside this specification without updating SPEC.md first.*
