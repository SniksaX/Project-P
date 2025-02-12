from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 3333
    DATABASE_NAME: str = "xxx"
    DATABASE_USER: str = "xxx"
    DATABASE_PASSWORD: str = "xxx"
    EMAIL_FROM: str = "Email_To_Send_From"
    EMAIL_PASSWORD: str = "Password of app created(check documentation)"
    VERIFICATION_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    class Config:
        env_file = ".env"


settings = Settings()
