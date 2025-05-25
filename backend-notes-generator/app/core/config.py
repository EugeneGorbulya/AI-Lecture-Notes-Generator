from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    DOCS_PASSWORD: str = "password"
    PROJECT_NAME: str = "Backend Notes Generator"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for Backend Notes Generator"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 6000
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 6000
    OPENAI_API_URL: str = "http://localhost:1234/v1/chat/completions"
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
