import asyncio
import logging

from tasks.celery import app


@app.task(queue="push_queue")
def send_push_notification(text: str, user_id: int):
    logging.info(
        f"sending push to user with id: {user_id} about new news with title: {text}"
    )
    asyncio.run(send_push_to_user(text, user_id))
    logging.info(
        f"push was sent successfully to user with id: {user_id} about a new news with title: {text}"
    )


async def send_push_to_user(text: str, user_id: int):
    await asyncio.sleep(0.15)
