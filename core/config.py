from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/user_db"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()