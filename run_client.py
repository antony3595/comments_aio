import asyncio
import logging
import time

from pydantic import ValidationError

import config
from clients.jph_client import get_json_placeholder_client
from clients.tcp_client import TCPServerClient
from schema.json_placeholder import Post, Comment

logger = logging.getLogger(__name__)


async def produce_comment(comment: Comment, queue: asyncio.Queue):
    logger.info(f"Producing comment {comment.id}")
    await queue.put(comment)


async def consume_comments(q: asyncio.Queue) -> None:
    while True:
        comment = await q.get()
        logger.info(f"Consuming comment {comment.id}")
        client = TCPServerClient()
        try:
            await client.update_post_by_comment(comment)
        except ValidationError as e:
            logger.error(f"TCP server error: {repr(e)}")
        except Exception as e:
            logger.error(f"Consuming error: {repr(e)}")

        q.task_done()


async def process_post_comments(post: Post, queue: asyncio.Queue):
    async with get_json_placeholder_client() as client:
        comments = []
        try:
            comments = await client.get_post_comments(post.id)
        except Exception as e:
            logger.exception(
                "Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {})
            )

    producers = [produce_comment(comment, queue) for comment in comments]
    await asyncio.gather(*producers)


async def start_consumers(queue: asyncio.Queue):
    consumers = [asyncio.create_task(consume_comments(queue)) for n in range(int(config.settings.CONSUMERS_COUNT))]
    logger.info(f"Starting {config.settings.CONSUMERS_COUNT} consumers")
    return consumers


async def main():
    start = time.perf_counter()

    post_comments_tasks = []
    queue = asyncio.Queue()
    consumers = await start_consumers(queue)

    async with get_json_placeholder_client() as client:
        posts = await client.get_posts()
        for post in posts:
            post_comments_tasks.append(process_post_comments(post, queue=queue))

    await asyncio.gather(*post_comments_tasks)
    await queue.join()
    for c in consumers:
        c.cancel()
    duration = time.perf_counter() - start
    logger.info(f"Program completed in {duration:0.2f} seconds.")


if __name__ == '__main__':
    asyncio.run(main())
