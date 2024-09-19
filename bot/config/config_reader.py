import os
from pydantic import SecretStr, RedisDsn, PostgresDsn, BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr
    admin_id: SecretStr
    redis_dsn: RedisDsn
    db_dsn: PostgresDsn
    is_echo: bool = True

    class Config:
        env_file = os.path.expanduser(".env")
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


config = Settings()
