"""TaskSum frontend — Streamlit UI.

Cycle 3: UI + wiring to backend endpoints via requests.
Cycle 4: graceful error displays.
"""

import requests
import streamlit as st

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="TaskSum", page_icon="✅")
st.title("✅ TaskSum")
st.caption("Complete tasks. Get a one-paragraph summary of your day.")

# --- Add task ---
with st.form("add_task_form", clear_on_submit=True):
    new_task = st.text_input("New task", placeholder="e.g. Write project spec")
    submitted = st.form_submit_button("Add task")

if submitted:
    if not new_task.strip():
        st.warning("Task can't be empty.")
    else:
        try:
            resp = requests.post(f"{API_BASE}/tasks", json={"title": new_task}, timeout=5)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            st.error(f"Couldn't add task — is the backend running? ({e})")

# --- List tasks ---
st.subheader("Your tasks")
try:
    tasks_resp = requests.get(f"{API_BASE}/tasks", timeout=5)
    tasks_resp.raise_for_status()
    tasks = tasks_resp.json()
except requests.exceptions.RequestException as e:
    tasks = []
    st.error(f"Couldn't load tasks — is the backend running? ({e})")

if not tasks:
    st.info("No tasks yet. Add one above.")
else:
    for task in tasks:
        col1, col2 = st.columns([5, 1])
        with col1:
            label = f"~~{task['title']}~~" if task["completed"] else task["title"]
            st.markdown(label)
        with col2:
            if not task["completed"]:
                if st.button("Done", key=f"done_{task['id']}"):
                    try:
                        r = requests.patch(
                            f"{API_BASE}/tasks/{task['id']}/complete", timeout=5
                        )
                        r.raise_for_status()
                        st.rerun()
                    except requests.exceptions.RequestException as e:
                        st.error(f"Couldn't update task: {e}")

# --- Summary ---
st.divider()
st.subheader("Daily summary")
if st.button("✨ Summarize completed tasks"):
    with st.spinner("Generating summary..."):
        try:
            r = requests.post(f"{API_BASE}/summary", timeout=30)
            if r.status_code == 400:
                st.warning(r.json().get("detail", "No completed tasks yet."))
            elif r.status_code == 502:
                st.error(f"AI service error: {r.json().get('detail')}")
            else:
                r.raise_for_status()
                st.success(r.json()["summary"])
        except requests.exceptions.RequestException as e:
            st.error(f"Couldn't reach backend: {e}")
