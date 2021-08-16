from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL : str = "sqlite:///./sql_app.db"

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()