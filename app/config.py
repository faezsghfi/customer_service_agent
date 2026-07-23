
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    OPENAI_API_KEY: str

    OPENAI_MODEL: str = "gpt-4.1-mini"

    QDRANT_URL: str = "http://localhost:6333"

    QDRANT_COLLECTION: str = "customer_support"

    EMBEDDING_MODEL: str = "BAAI/bge-m3"


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
