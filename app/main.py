from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.database.databas import Task, create_tables, get_db


create_tables()
app = FastAPI(
     title="Production-Ready Task Manager API",
     description="A professional Task Manager API built with FastAPI and SQLAlchemy",
     version="1.0.0"
)

#  PYDANTIC SCHEMAS (DATA VALIDATION)
class TaskRequest(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: Optional[bool] = False


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    date: datetime
    is_completed: bool

    class Config:
        from_attributes = True 


# ১. Create Task 
@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskRequest, db: Session = Depends(get_db)):
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        is_completed=task_data.is_completed
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# ২. Get All Tasks 
@app.get("/tasks", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

# ৩. Get Single Task ()
@app.get("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_single_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task with id {task_id} not found"
        )
    return task



# ৪. Update Task ()
@app.put("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(task_id: int, update_data: TaskRequest, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task with id {task_id} not found"
        )
    
    # data update
    task.title = update_data.title
    task.description = update_data.description
    task.is_completed = update_data.is_completed
    
    db.commit()
    db.refresh(task)
    return task

# ৫. Delete Task ()
@app.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task with id {task_id} not found"
        )
    
    db.delete(task)
    db.commit()
    return {"message": f"Task with id {task_id} has been deleted successfully"}





























