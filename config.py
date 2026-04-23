from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    PJ_NAME: str
    DB_PATH: str
    debug: bool


    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    CACHE_EXPIRE: int

    SECRET_KEY: str
    TOKEN_EXPIRE: int

    class Config:
        env_file = '.env'

settings = Settings()