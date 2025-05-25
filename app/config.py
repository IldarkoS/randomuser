import os

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
        env_file = os.environ.get("ENV_FILE", ".env")

    @property
    def DATABASE_DSN(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()