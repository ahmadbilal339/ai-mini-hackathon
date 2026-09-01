"""
FastAPI application for TaskSum - AI To-Do Summarizer.
"""
from typing import List
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from backend.models import Task, TaskCreate
from backend.llm import generate_summary  

app = FastAPI(title="TaskSum API", description="AI To-Do Summarizer")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (no database - MVP scope)
tasks_db = []
task_id_counter = 1

@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {"message": "TaskSum API is running", "status": "healthy"}

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    """Get all tasks."""
    return tasks_db

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """Create a new task."""
    global task_id_counter
    
    title = task.title.strip()
    
    new_task = Task(
        id=task_id_counter,
        title=title,
        completed=False
    )
    tasks_db.append(new_task)
    task_id_counter += 1
    
    return new_task

@app.patch("/tasks/{task_id}/complete", response_model=Task)
async def complete_task(task_id: int):
    """Mark a task as complete."""
    for task in tasks_db:
        if task.id == task_id:
            task.completed = True
            return task
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found"
    )


@app.post("/summary")
async def generate_summary_endpoint():
    """
    Generate an AI summary of all completed tasks.
    """
    # Get completed tasks
    completed_tasks = [task.title for task in tasks_db if task.completed]
    
    # Generate summary using Gemini
    summary = generate_summary(completed_tasks)
    
    return {"summary": summary}