
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration
    """

    OPENAI_API_KEY: str

    OPENAI_MODEL: str = "gpt-4.1-mini"

    QDRANT_URL: str = "http://localhost:6333"

    QDRANT_COLLECTION: str = "customer_support"

    EMBEDDING_MODEL: str = "BAAI/bge-m3"


    class Config:
        env_file = ".env"


settings = Settings()
