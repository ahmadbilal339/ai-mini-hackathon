"""
Pydantic schemas for the TaskSum API.
"""
from pydantic import BaseModel, Field, field_validator

class TaskCreate(BaseModel):
    """Request body for POST /tasks."""
    title: str = Field(..., min_length=1, description="Task title")
    
    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Task title cannot be empty or whitespace-only.")
        return value

class Task(BaseModel):
    """A task returned by the API."""
    id: int
    title: str
    completed: bool = False