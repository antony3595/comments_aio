from celery import Celery
from kombu import Queue

from config import settings

app = Celery(__name__, broker=settings.REDIS_URL.get_secret_value(), backend=settings.REDIS_URL.get_secret_value())

app.conf.task_queues = [
    Queue("ingest_queue"),
    Queue("push_queue")
]
