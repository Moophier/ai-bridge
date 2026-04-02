from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    model: str = "llama3-8b"
    prompt: str
    max_tokens: int = 100

class TaskResponse(BaseModel):
    task_id: str
    model: str
    prompt: str
    max_tokens: int
    status: str
    result: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

class TaskSubmitResponse(BaseModel):
    task_id: str
    status: str
