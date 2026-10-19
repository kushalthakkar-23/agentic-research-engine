from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_TITLE: str = "Project Atlas Report Copilot"
    API_VERSION: str = "1.0.0"
    API_KEY: str = "atlas-prod-secret-key-102938"
    EMBEDDING_DIMENSION: int = 1536

settings = Settings()
