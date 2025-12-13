from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]  # backend/


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI News Dashboard"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str

    # Database
    DATABASE_URL: str

    # Hugging Face
    HUGGINGFACE_API_KEY: str
    HUGGINGFACE_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Embeddings
    HUGGINGFACE_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384

    # Rate limiting
    MAX_REQUESTS_PER_MINUTE: int = 60  # default; override via env if needed

    # CORS (string, then parsed)
    BACKEND_CORS_ORIGINS_RAW: Optional[str] = None

    @property
    def BACKEND_CORS_ORIGINS(self) -> List[str]:
        if not self.BACKEND_CORS_ORIGINS_RAW:
            return []
        return [o.strip() for o in self.BACKEND_CORS_ORIGINS_RAW.split(",")]

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
