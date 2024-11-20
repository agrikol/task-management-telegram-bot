import os
from pydantic import (
    SecretStr,
    RedisDsn,
    PostgresDsn,
    field_validator,
    NatsDsn,
)

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    bot_token: SecretStr
    admin_id: str
    redis_dsn: RedisDsn
    db_dsn: PostgresDsn
    is_echo: bool = True
    nats_servers: str
    nats_delayed_consumer_subject: str
    nats_delayed_consumer_stream: str
    nats_delayed_consumer_durable_name: str

    @field_validator("admin_id")
    def parse_admin_id(cls, value: str) -> list[int]:
        return [int(admin_id) for admin_id in value.split(",")]

    class Config:
        env_file = os.path.expanduser(".env")
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
        extra = "ignore"
