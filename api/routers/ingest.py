import asyncio
import logging
import random
from typing import List, Any, Annotated

from fastapi import APIRouter, Body
from fastapi.params import Depends
from pydantic import Json
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import ServiceAccountAuth
from db.connections.postgres import get_db
from db.models.news import NewsTypeEnum
from schema.db.service_account import ServiceAccountSchema
from services.raw_news.raw_news import RawNewsService
from tasks.raw_news import process_raw_news

logger = logging.getLogger()
ingest_router = APIRouter(prefix="/ingest", tags=["ingest"])


def generate_fake_ingest_body():
    body = []
    categories = [e.value for e in NewsTypeEnum]

    for i in range(1, 1000):
        body.append('{{"title": "ingested news {}","categories": ["{}"]}}'.format(i, random.choice(categories)))
    return body


@ingest_router.post("/news", response_model=List[str])
async def ingest_raw_news(service_account: Annotated[ServiceAccountSchema, Depends(ServiceAccountAuth())],
                          body: List[Json[Any]] = Body(example=generate_fake_ingest_body()),
                          db: AsyncSession = Depends(get_db),
                          ):
    logger.info(f"Ingesting raw news data {body}")

    raw_news_service = RawNewsService()
    tasks = [raw_news_service.create_raw_news(db, service_account.id, data_item) for data_item in body]
    results = await asyncio.gather(*tasks)
    await db.commit()

    # TODO do it in thread
    shared_task_ids = []

    for raw_news in results:
        shared_task = process_raw_news.delay(raw_news.id)
        shared_task_ids.append(shared_task.id)
    return shared_task_ids
