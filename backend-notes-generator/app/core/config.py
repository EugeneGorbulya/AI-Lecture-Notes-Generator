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
    class Config:
        env_file = ".env"

settings = Settings()
