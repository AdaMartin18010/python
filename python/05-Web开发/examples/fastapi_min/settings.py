from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "fastapi-min"
    env: str = "dev"  # dev/stage/prod
    debug: bool = True

    class Config:
        env_prefix = "APP_"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # 从环境变量加载 APP_*


