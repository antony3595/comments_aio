import asyncio
import logging
from typing import List, Any, Annotated

from fastapi import APIRouter, Body
from fastapi.params import Depends
from pydantic import Json
from sqlalchemy.ext.asyncio import AsyncSession
from tasks.raw_news import process_raw_news
from api.dependencies.auth import ServiceAccountAuth
from db.connections.postgres import get_db
from schema.db.service_account import ServiceAccountSchema
from services.raw_news.raw_news import RawNewsService

logger = logging.getLogger()
ingest_router = APIRouter(prefix="/ingest", tags=["ingest"])


@ingest_router.post("/news", response_model=List[str])
async def ingest_raw_news(service_account: Annotated[ServiceAccountSchema, Depends(ServiceAccountAuth())],
                          body: List[Json[Any]] = Body(example=['{"foo": "bar"}']),
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
