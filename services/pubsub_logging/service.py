from datetime import datetime
from typing import List

import click
from redis.typing import ResponseT

from clients.redis.client import get_redis_client


class PubSubLoggingService:

    async def listen_messages(self, channels: List[str]) -> None:
        async with get_redis_client() as r, r.pubsub() as p:
            for channel in channels:
                await p.subscribe(channel)
                click.echo(f'Subscribed to "{channel}" channel')
            while True:
                message = await p.get_message(ignore_subscribe_messages=True)
                if message is not None and "data" in message:
                    data = message.get("data").decode("utf-8")
                    log_time = click.style(f"[{datetime.now()}]", fg="green")
                    log_channel = click.style(
                        f"[Channel: {message.get('channel').decode()}]",
                        fg="blue",
                    )

                    click.echo(f"{log_time} | {log_channel} {str(data)}")

    async def log(self, channel: str, message: str) -> ResponseT:
        async with get_redis_client() as r:
            return await r.publish(channel, message)


def get_pub_sub_logging_service() -> PubSubLoggingService:
    return PubSubLoggingService()
