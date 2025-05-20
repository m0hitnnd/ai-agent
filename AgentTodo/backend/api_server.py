from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'nlp'))
import db_utils
from nlp.agent_todo_nlp import get_llm_command_analysis
from fastapi.middleware.cors import CORSMiddleware

# Ensure DB is initialized
try: 
    db_utils.init_db()
except Exception as e:
    print(f"Warning: Could not initialize DB: {e}")

app = FastAPI()

# Add CORS middleware to allow requests from your iOS app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your iOS app's domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskCreate(BaseModel):
    task: str
    time: Optional[int] = None

class Task(BaseModel):
    id: int
    task: str
    time: Optional[int]
    is_completed: bool = False
    actual_time: Optional[int] = None

class TaskUpdate(BaseModel):
    task: str

class TaskComplete(BaseModel):
    actual_time: int

class EstimatedTime(BaseModel):
    estimated_time: int

@app.get("/tasks", response_model=List[Task])
def list_tasks():
    rows = db_utils.get_all_tasks_with_ids()
    return [Task(id=row[0], task=row[1], time=row[2], is_completed=row[3] if len(row) > 3 else False, 
                actual_time=row[4] if len(row) > 4 else None) for row in rows]

@app.get("/estimate", response_model=EstimatedTime)
def estimate_task_time(task: str = Query(..., description="The task to estimate time for")):
    analysis = get_llm_command_analysis(task)
    estimated_time = analysis.get("estimated_time")
    # Fallback if LLM fails to provide time
    time_value = estimated_time if estimated_time is not None else 60
    return EstimatedTime(estimated_time=time_value)

@app.post("/tasks", response_model=Task)
def add_task(task: TaskCreate):
    # If time is not provided, estimate using LLM
    if task.time is None:
        analysis = get_llm_command_analysis(task.task)
        estimated_time = analysis.get("estimated_time")
        # Fallback if LLM fails to provide time
        time_value = estimated_time if estimated_time is not None else 60
    else:
        time_value = task.time

    db_utils.add_task_to_db(task.task, time_value)
    row = db_utils.get_last_inserted_task()
    return Task(id=row[0], task=row[1], time=row[2])

@app.post("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int, task_complete: TaskComplete):
    # Get the existing task to verify it exists
    existing_task = db_utils.get_task_by_id(task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update the task in the database to mark as completed and set actual time
    updated = db_utils.complete_task(task_id, task_complete.actual_time)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to complete task")
    
    # Get and return the updated task
    updated_task = db_utils.get_task_by_id(task_id)
    return Task(id=updated_task[0], task=updated_task[1], time=updated_task[2], 
                is_completed=updated_task[3] if len(updated_task) > 3 else True,
                actual_time=updated_task[4] if len(updated_task) > 4 else task_complete.actual_time)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    deleted = db_utils.delete_task_by_id(task_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    # Get the existing task to verify it exists
    existing_task = db_utils.get_task_by_id(task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Re-estimate time using LLM
    analysis = get_llm_command_analysis(task_update.task)
    estimated_time = analysis.get("estimated_time")
    # Fallback if LLM fails to provide time
    time_value = estimated_time if estimated_time is not None else 60
    
    # Update the task in the database
    updated = db_utils.update_task(task_id, task_update.task, time_value)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update task")
    
    # Get and return the updated task
    updated_task = db_utils.get_task_by_id(task_id)
    return Task(id=updated_task[0], task=updated_task[1], time=updated_task[2])

# Add a simple health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# To run: uvicorn api_server:app --reload --port 8000
# In production, this is handled by the Procfile and environment variables
