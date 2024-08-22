import os
from pydantic import SecretStr, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr
    redis_dsn: RedisDsn

    class Config:
        env_file = os.path.expanduser(".env")
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
