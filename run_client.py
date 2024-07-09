import asyncio
import logging

from aiohttp import ClientSession

import conf
from clients.json_placeholder_client.client import JsonPlaceholderClient
from clients.tcp_client import TCPServerClient

logger = logging.getLogger(__name__)


async def produce_comment(comment: dict, queue: asyncio.Queue):
    logger.info(f"Producing comment {comment['id']}")
    await queue.put(comment)


async def consume_comments(q: asyncio.Queue) -> None:
    while True:
        comment = await q.get()
        logger.info(f"Consuming comment {comment['id']}")
        client = TCPServerClient()
        await client.update_comment(comment)
        q.task_done()


async def process_post_comments(post_id: int, session: ClientSession, queue: asyncio.Queue):
    client = JsonPlaceholderClient()
    comments = []
    try:
        comments = await client.get_post_comments(post_id, session)
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {})
        )

    producers = [produce_comment(comment, queue) for comment in comments]
    await asyncio.gather(*producers)


async def start_consumers(queue: asyncio.Queue):
    consumers = [asyncio.create_task(consume_comments(queue)) for n in range(int(conf.CONSUMERS_COUNT))]
    logger.info(f"Starting {conf.CONSUMERS_COUNT} consumers")
    return consumers


async def main():
    client = JsonPlaceholderClient()
    post_comments_tasks = []
    queue = asyncio.Queue()
    consumers = await start_consumers(queue)

    async with ClientSession() as session:
        posts = await client.get_posts(session)
        for post in posts:
            post_comments_tasks.append(process_post_comments(post["id"], session, queue=queue))

        await asyncio.gather(*post_comments_tasks)
    await queue.join()
    for c in consumers:
        c.cancel()


if __name__ == '__main__':
    asyncio.run(main())
