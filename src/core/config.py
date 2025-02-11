from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 3333
    DATABASE_NAME: str = "project_name"
    DATABASE_USER: str = "user_name"
    DATABASE_PASSWORD: str = "password"

    class Config:
        env_file = ".env"


settings = Settings()
