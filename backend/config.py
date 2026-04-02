import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Redis配置
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # 数据库配置
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ai_bridge.db")
    
    # API配置
    API_TITLE = "AI算力匹配桥 API"
    API_VERSION = "1.0.0"
    
    # 支持的模型
    SUPPORTED_MODELS = ["llama3-8b", "mistral-7b", "qwen-7b"]
    
    # 默认配置
    DEFAULT_MAX_TOKENS = 100
