import os
import asyncio
from redis import Redis
from rq import Queue
from config import Config

try:
    redis_conn = Redis.from_url(Config.REDIS_URL)
    redis_conn.ping()
    task_queue = Queue("ai-tasks", connection=redis_conn)
    REDIS_AVAILABLE = True
except Exception as e:
    print(f"Redis not available, using in-memory queue: {e}")
    task_queue = None
    REDIS_AVAILABLE = False

_task_results = {}
_task_queue_list = []

def mock_inference(model: str, prompt: str, max_tokens: int) -> str:
    """模拟推理（实际替换为vLLM调用）"""
    import time
    time.sleep(2)
    return f"[{model}] 生成结果: {prompt[:50]}..."

def process_task(task_id: str, model: str, prompt: str, max_tokens: int):
    """后台任务处理函数"""
    from database import SessionLocal
    from models import Task
    from datetime import datetime
    
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.task_id == task_id).first()
        if task:
            task.status = "processing"
            db.commit()
            
            result = mock_inference(model, prompt, max_tokens)
            
            task.result = result
            task.status = "completed"
            task.completed_at = datetime.now()
            db.commit()
    finally:
        db.close()

def submit_task(task_id: str, model: str, prompt: str, max_tokens: int):
    """提交任务（Redis或内存队列）"""
    if REDIS_AVAILABLE and task_queue:
        task_queue.enqueue(process_task, task_id, model, prompt, max_tokens)
    else:
        _task_queue_list.append((task_id, model, prompt, max_tokens))
        
def get_queued_tasks():
    """获取队列中的任务"""
    if REDIS_AVAILABLE:
        return []
    return _task_queue_list
