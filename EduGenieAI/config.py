from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GEMINI_API_KEY: str = Field(
        default="",
        description="Google Gemini API key",
    )

    GEMINI_MODEL: str = Field(
        default="gemini-3.8-flash",
        description="Gemini model used by EduGenie",
    )

    EXPLANATION_PROVIDER: str = Field(
        default="gemini",
        description="gemini or local",
    )

    LOCAL_EXPLANATION_MODEL: str = Field(
        default="MBZUAI/LaMini-Flan-T5-783M",
        description="Optional local explanation model",
    )

    MAX_INPUT_CHARS: int = Field(
        default=20000,
        ge=1000,
        le=100000,
    )

    REQUEST_TIMEOUT_SECONDS: int = Field(
        default=90,
        ge=10,
        le=600,
    )

    CORS_ORIGINS: str = Field(
        default="http://127.0.0.1:8000,http://localhost:8000"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()