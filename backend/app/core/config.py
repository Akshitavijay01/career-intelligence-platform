from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database - SQLite for local development
    DATABASE_URL: str = "sqlite:///./career_intelligence.db"

    # JWT Configuration
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # File Upload
    MAX_FILE_SIZE_MB: int = 5
    UPLOAD_DIR: str = "./uploads"

    # AI/ML Configuration
    # Use lighter model for local development or disable if needed
    SENTENCE_TRANSFORMERS_MODEL: str = "all-MiniLM-L6-v2"
    USE_LOCAL_EMBEDDINGS: bool = True  # Use simple word-based similarity instead

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"]

    # Environment
    DEBUG: bool = True
    LOG_LEVEL: str = "info"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()