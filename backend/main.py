from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from config import Config
from database import get_db, engine, Base
from models import Task
from schemas import TaskCreate, TaskResponse, TaskSubmitResponse
from tasks import submit_task, get_queued_tasks, process_task, REDIS_AVAILABLE, _task_queue_list

Base.metadata.create_all(bind=engine)

app = FastAPI(title=Config.API_TITLE, version=Config.API_VERSION)

@app.post("/submit", response_model=TaskSubmitResponse)
def submit_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    if task_data.model not in Config.SUPPORTED_MODELS:
        raise HTTPException(status_code=400, detail=f"不支持的模型: {task_data.model}")
    
    task_id = str(uuid.uuid4())
    task = Task(
        task_id=task_id,
        model=task_data.model,
        prompt=task_data.prompt,
        max_tokens=task_data.max_tokens,
        status="queued"
    )
    db.add(task)
    db.commit()
    
    if REDIS_AVAILABLE:
        submit_task(task_id, task_data.model, task_data.prompt, task_data.max_tokens)
    else:
        import threading
        thread = threading.Thread(target=process_task, args=(task_id, task_data.model, task_data.prompt, task_data.max_tokens))
        thread.start()
    
    return TaskSubmitResponse(task_id=task_id, status="queued")

@app.get("/result/{task_id}", response_model=TaskResponse)
def get_result(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    return task

@app.get("/models")
def get_models():
    return {"models": Config.SUPPORTED_MODELS}

@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).order_by(Task.created_at.desc()).limit(50).all()
    return tasks

@app.get("/")
def root():
    return {"message": "AI算力匹配桥 API", "version": Config.API_VERSION}

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "redis_available": REDIS_AVAILABLE,
        "queue_length": len(_task_queue_list) if not REDIS_AVAILABLE else "using redis"
    }
