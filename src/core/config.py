from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "..."
    ALGORITHM: str = "..."
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_HOST: str = "..."
    DATABASE_PORT: int = ...
    DATABASE_NAME: str = "..."
    DATABASE_USER: str = "..."
    DATABASE_PASSWORD: str = "..."
    EMAIL_FROM: str = "..."
    EMAIL_PASSWORD: str = "..."
    VERIFICATION_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    TMDB_API_KEY: str = "..."
    TMDB_API_KEY_V4: str = "..."

    class Config:
        env_file = ".env"


settings = Settings()
