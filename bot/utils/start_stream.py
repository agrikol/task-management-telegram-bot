import asyncio
from nats.aio.client import Client
from nats.js import JetStreamManager
from nats.js.errors import NotFoundError
from nats.js.api import StreamConfig


async def create_stream(js: JetStreamManager, stream_name: str, subjects: list) -> str:
    try:
        stream_info = await js.stream_info(stream_name)
        return f"Stream '{stream_info.config.name}' already exists."

    except NotFoundError as e:
        stream_config = StreamConfig(
            name=stream_name,
            subjects=subjects,
            retention="workqueue",
            max_bytes=200 * 1024 * 1024,
            max_msg_size=20 * 1024 * 1024,
            storage="file",
            allow_direct=True,
        )
        await js.add_stream(stream_config)

        return f"Stream '{stream_name}' created successfully."
