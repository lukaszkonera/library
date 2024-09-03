from pathlib import Path

import dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    UVICORN_RELOAD: bool = False
    DEBUG: bool = False
    SERVICE_PORT: int = 8000

    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_MAX_POOLSIZE: int = 5

    def sql_alchemy_database_url(self):
        return f"{self.POSTGRES_HOST}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@postgres:"\
                    f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    def sql_alchemy_engine_options(self):
        return {
    "pool_pre_ping": True,
    "pool_size": self.POSTGRES_MAX_POOLSIZE,
    "max_overflow": 4,
    "pool_timeout": 10,
    "pool_recycle": 300,
}

    class Config:
        env_file = Path(BASE_DIR, "settings", ".env")
        dotenv.load_dotenv(env_file)


settings = Settings()
