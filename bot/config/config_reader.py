import os
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr

    class Config:
        env_file = os.path.expanduser("/.env")
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


config = Settings()
