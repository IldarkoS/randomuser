from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RANDOM_USER_API_URL: str
    PAGE_LIMIT: int

    USERS_ON_START: int

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
settings.__dict__["DATABASE_DSN"] = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"