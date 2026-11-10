from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "VerifyFlow"
    app_env: str = "development"
    cors_origins: List[str] | str = ["http://localhost:5173", "http://127.0.0.1:5173"]

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/verifyflow"

    ocr_provider: str = "tesseract"
    llm_provider: str = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    id_hash_secret: str = "dev-only-secret"
    kyc_retention_days: int = 7

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | List[str]) -> List[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

