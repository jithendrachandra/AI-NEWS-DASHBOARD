from typing import List
from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl

BASE_DIR = Path(__file__).resolve().parents[2]  # -> backend/


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI News Dashboard"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str

    # Database
    DATABASE_URL: str

    # Hugging Face API
    HUGGINGFACE_API_KEY: str
    HUGGINGFACE_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"
    HUGGINGFACE_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = 30

    # Embedding Settings
    EMBEDDING_DIMENSION: int = 384

    # CORS (Pydantic v2 expects JSON here)
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    class Config:
        case_sensitive = True
        env_file = BASE_DIR / ".env"


settings = Settings()
