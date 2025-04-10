import asyncio
from datetime import datetime

import click

from services.pubsub_logging.service import get_pub_sub_logging_service


@click.command()
@click.argument("channels", nargs=-1, type=str)
def logs(channels: tuple[str]) -> None:
    asyncio.run(_logs(channels))


async def _logs(channels):
    try:
        service = get_pub_sub_logging_service()
        await service.listen_messages(channels)

    except KeyboardInterrupt:
        click.echo(f"unsubscribed from: {channels}")
        click.echo(
            click.style(
                f"Have a nice {datetime.now().strftime('%A')}, my dude :)",
                fg="green",
                italic=True,
            )
        )


if __name__ == "__main__":
    logs()
