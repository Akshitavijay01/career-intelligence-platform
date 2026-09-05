from pydantic_settings import BaseSettings
from typing import List
import json

def parse_cors_origins(value: str) -> List[str]:
    """Parse CORS_ORIGINS from a JSON array string or a comma-separated string.

    Render injects CORS_ORIGINS as an env string. pydantic-settings JSON-decodes
    List[str] fields from env vars and crashes if the value is not valid JSON, so
    we treat the raw value as a string here and parse it defensively.
    """
    if not value or not value.strip():
        return []
    s = value.strip()
    # JSON array form: ["http://a", "http://b"]
    if s.startswith("[") and s.endswith("]"):
        try:
            items = json.loads(s)
            if isinstance(items, list):
                return [str(x).strip() for x in items if str(x).strip()]
        except Exception:
            pass
    # comma-separated form: http://a,http://b
    return [part.strip() for part in s.split(",") if part.strip()]

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

    # CORS - kept as a raw string so pydantic-settings does not try to json.loads it
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"

    @property
    def cors_origins_list(self) -> List[str]:
        return parse_cors_origins(self.CORS_ORIGINS)

    # Environment
    DEBUG: bool = True
    LOG_LEVEL: str = "info"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()