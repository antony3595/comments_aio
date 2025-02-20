from celery import Celery
from celery.schedules import crontab
from kombu import Queue

from config import settings

app = Celery(__name__,
             broker=settings.REDIS_URL.get_secret_value(),
             backend=settings.REDIS_URL.get_secret_value(),
             )

app.conf.task_queues = [
    Queue("ingest_queue"),
    Queue("push_queue")
]


app.conf.beat_schedule = {
    "process_stuck_raw_news": {
        "task": "tasks.stuck_raw_news.process_stuck_raw_news_task",
        "schedule": crontab(minute="*/1"),
    }
}

app.autodiscover_tasks()