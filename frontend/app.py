"""TaskSum frontend — Streamlit UI.

A ledger-inspired redesign: dark ink background, warm gold accent,
tasks laid out as ruled lines rather than boxed cards, and the AI
summary presented as a pulled note rather than a generic alert.

Wiring to the FastAPI backend is unchanged from the original —
same endpoints, same error handling, same behavior.
"""

import requests
import streamlit as st

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="TaskSum", page_icon="✦", layout="centered")

# ----------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap');

    :root {
        --ink:        #12171C;
        --ink-panel:  #1A2028;
        --paper:      #ECE7DC;
        --paper-dim:  #A9A79D;
        --gold:       #D4A73A;
        --sage:       #7FAE8C;
        --rule:       #2C333C;
    }

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: var(--ink);
        color: var(--paper);
    }

    /* Kill Streamlit's default top padding / chrome */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 4rem;
        max-width: 640px;
    }
    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }

    /* ---- Masthead ---- */
    .ts-masthead {
        margin-bottom: 0.25rem;
    }
    .ts-masthead h1 {
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 2.6rem;
        letter-spacing: -0.01em;
        color: var(--paper);
        margin: 0;
        line-height: 1.1;
    }
    .ts-masthead p {
        font-family: 'Inter', sans-serif;
        color: var(--paper-dim);
        font-size: 0.98rem;
        margin: 0.35rem 0 0 0;
    }
    .ts-rule {
        border: none;
        border-top: 1px solid var(--rule);
        margin: 1.4rem 0 1.6rem 0;
    }

    /* ---- Section labels ---- */
    .ts-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.78rem;
        color: var(--gold);
        font-weight: 600;
        letter-spacing: 0.01em;
        margin: 0 0 0.6rem 0;
    }

    /* ---- Text input ---- */
    div[data-testid="stForm"] {
        border: none;
        padding: 0;
    }
    .stTextInput input {
        background: var(--ink-panel);
        color: var(--paper);
        border: 1px solid var(--rule);
        border-radius: 3px;
        padding: 0.6rem 0.8rem;
    }
    .stTextInput input:focus {
        border-color: var(--gold);
        box-shadow: none;
    }
    .stTextInput input::placeholder { color: var(--paper-dim); }

    /* ---- Buttons ---- */
    .stButton button, .stFormSubmitButton button {
        background: transparent;
        color: var(--gold);
        border: 1px solid var(--gold);
        border-radius: 3px;
        padding: 0.4rem 1.1rem;
        font-weight: 500;
        font-size: 0.9rem;
        transition: background 0.15s ease, color 0.15s ease;
    }
    .stButton button:hover, .stFormSubmitButton button:hover {
        background: var(--gold);
        color: var(--ink);
    }
    .stButton button:active, .stFormSubmitButton button:active {
        background: var(--gold);
        color: var(--ink);
    }

    /* Small "Done" buttons in the task rows */
    .ts-row-btn button {
        border-color: var(--rule);
        color: var(--paper-dim);
        padding: 0.25rem 0.7rem;
        font-size: 0.78rem;
    }
    .ts-row-btn button:hover {
        border-color: var(--sage);
        background: var(--sage);
        color: var(--ink);
    }

    /* ---- Task rows ---- */
    .ts-task-row {
        display: flex;
        align-items: center;
        padding: 0.85rem 0;
        border-bottom: 1px solid var(--rule);
    }
    .ts-task-title {
        font-size: 1rem;
        color: var(--paper);
    }
    .ts-task-title.done {
        color: var(--paper-dim);
        text-decoration: line-through;
        text-decoration-color: var(--sage);
    }
    .ts-check {
        color: var(--sage);
        margin-right: 0.55rem;
        font-size: 1rem;
    }
    .ts-check.open {
        color: var(--rule);
    }

    /* ---- Progress ---- */
    .ts-progress-line {
        color: var(--paper-dim);
        font-size: 0.88rem;
        margin: 0.9rem 0 0.5rem 0;
    }
    .ts-progress-bar-track {
        height: 3px;
        background: var(--rule);
        border-radius: 2px;
        overflow: hidden;
    }
    .ts-progress-bar-fill {
        height: 100%;
        background: var(--gold);
    }

    /* ---- Empty state ---- */
    .ts-empty {
        color: var(--paper-dim);
        font-style: italic;
        padding: 1rem 0;
        border-bottom: 1px solid var(--rule);
    }

    /* ---- Summary note ---- */
    .ts-summary-note {
        border-left: 2px solid var(--gold);
        padding: 0.3rem 0 0.3rem 1.1rem;
        margin-top: 0.6rem;
    }
    .ts-summary-note p {
        font-family: 'Fraunces', serif;
        font-style: italic;
        font-size: 1.12rem;
        line-height: 1.55;
        color: var(--paper);
        margin: 0;
    }

    /* ---- Alerts (keep readable in dark theme) ---- */
    div[data-testid="stAlert"] {
        background: var(--ink-panel);
        border: 1px solid var(--rule);
        border-radius: 3px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Masthead
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="ts-masthead">
        <h1>TaskSum</h1>
        <p>Complete tasks. Get a one-paragraph summary of your day.</p>
    </div>
    <hr class="ts-rule">
    """,
    unsafe_allow_html=True,
)

# --- Add task ---
st.markdown('<div class="ts-label">ADD A TASK</div>', unsafe_allow_html=True)
with st.form("add_task_form", clear_on_submit=True):
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        new_task = st.text_input(
            "New task",
            placeholder="e.g. Write project spec",
            label_visibility="collapsed",
        )
    with col_btn:
        submitted = st.form_submit_button("Add")

if submitted:
    if not new_task.strip():
        st.warning("Task can't be empty.")
    else:
        try:
            resp = requests.post(f"{API_BASE}/tasks", json={"title": new_task}, timeout=5)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            st.error(f"Couldn't add task — is the backend running? ({e})")

st.markdown("<hr class='ts-rule'>", unsafe_allow_html=True)

# --- List tasks ---
st.markdown('<div class="ts-label">YOUR TASKS</div>', unsafe_allow_html=True)

try:
    tasks_resp = requests.get(f"{API_BASE}/tasks", timeout=5)
    tasks_resp.raise_for_status()
    tasks = tasks_resp.json()
except requests.exceptions.RequestException as e:
    tasks = []
    st.error(f"Couldn't load tasks — is the backend running? ({e})")

if not tasks:
    st.markdown('<div class="ts-empty">No tasks yet. Add one above.</div>', unsafe_allow_html=True)
else:
    completed_count = sum(1 for t in tasks if t["completed"])
    total_count = len(tasks)
    pct = int((completed_count / total_count) * 100) if total_count else 0

    st.markdown(
        f"""
        <div class="ts-progress-line">{completed_count} of {total_count} complete</div>
        <div class="ts-progress-bar-track">
            <div class="ts-progress-bar-fill" style="width:{pct}%;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for task in tasks:
        col_text, col_btn = st.columns([5, 1])
        with col_text:
            check = "✓" if task["completed"] else "○"
            check_class = "" if task["completed"] else "open"
            title_class = "done" if task["completed"] else ""
            st.markdown(
                f"""
                <div class="ts-task-row">
                    <span class="ts-check {check_class}">{check}</span>
                    <span class="ts-task-title {title_class}">{task['title']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_btn:
            if not task["completed"]:
                st.markdown('<div class="ts-row-btn">', unsafe_allow_html=True)
                if st.button("Done", key=f"done_{task['id']}"):
                    try:
                        r = requests.patch(
                            f"{API_BASE}/tasks/{task['id']}/complete", timeout=5
                        )
                        r.raise_for_status()
                        st.rerun()
                    except requests.exceptions.RequestException as e:
                        st.error(f"Couldn't update task: {e}")
                st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr class='ts-rule'>", unsafe_allow_html=True)

# --- Summary ---
st.markdown('<div class="ts-label">DAILY SUMMARY</div>', unsafe_allow_html=True)

if st.button("✦  Summarize completed tasks"):
    with st.spinner("Generating summary..."):
        try:
            r = requests.post(f"{API_BASE}/summary", timeout=30)
            if r.status_code == 400:
                st.warning(r.json().get("detail", "No completed tasks yet."))
            elif r.status_code == 502:
                st.error(f"AI service error: {r.json().get('detail')}")
            else:
                r.raise_for_status()
                summary_text = r.json()["summary"]
                st.markdown(
                    f"""
                    <div class="ts-summary-note">
                        <p>{summary_text}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        except requests.exceptions.RequestException as e:
            st.error(f"Couldn't reach backend: {e}")