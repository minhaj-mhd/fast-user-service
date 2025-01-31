from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "274e6b3c5e555c0a2d52fc91508ac7c3"
    DATABASE_URL: str = "postgresql+asyncpg://mj:mjpass@localhost:5432/smedia"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    SMTP_USER: str = "8452bd001@smtp-brevo.com"
    SMTP_PASSWORD: str = "nJyN5xIObvWSVqtA"
    SMTP_HOST: str = "smtp-relay.brevo.com"
    SMTP_PORT: int = 587
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PROJECT_NAME : str = "smfast"
    class Config:
        env_file = ".env"

settings = Settings()