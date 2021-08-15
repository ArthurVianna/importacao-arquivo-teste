import os

from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL : str = os.environ["DATABASE_URL"]

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()