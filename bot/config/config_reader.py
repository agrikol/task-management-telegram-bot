import os
from pydantic import SecretStr, RedisDsn, PostgresDsn, BaseModel, field_validator, Field
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    bot_token: SecretStr
    admin_id: str
    redis_dsn: RedisDsn
    db_dsn: PostgresDsn
    is_echo: bool = True

    @field_validator("admin_id")
    def parse_admin_id(cls, value: str) -> list[int]:
        return [int(admin_id) for admin_id in value.split(",")]

    class Config:
        env_file = os.path.expanduser(".env")
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


config = Settings()
