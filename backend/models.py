from sqlalchemy import Column, String, Integer, DateTime, Text
from datetime import datetime
from database import Base

class Task(Base):
    __tablename__ = "tasks"
    
    task_id = Column(String(36), primary_key=True)
    model = Column(String(50), nullable=False)
    prompt = Column(Text, nullable=False)
    max_tokens = Column(Integer, default=100)
    status = Column(String(20), default="queued")
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime, nullable=True)
