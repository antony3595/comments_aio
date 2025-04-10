import logging
import random
from typing import List, Any, Annotated

from fastapi import APIRouter, Body
from fastapi.params import Depends
from pydantic import Json
from starlette.responses import Response
from starlette.status import HTTP_200_OK

from api.dependencies.auth import ServiceAccountAuth
from db.connections.postgres import DBDependency
from db.models.news import NewsTypeEnum
from schema.db.service_account import ServiceAccountSchema
from services.pubsub_logging.service import get_pub_sub_logging_service
from services.raw_news.raw_news import RawNewsService
from tasks.raw_news import process_raw_news

logger = logging.getLogger()
ingest_router = APIRouter(prefix="/ingest", tags=["ingest"])


def generate_fake_ingest_body():
    body = []
    categories = [e.value for e in NewsTypeEnum]

    for i in range(1, 1000):
        body.append(
            '{{"title": "ingested news {}","categories": ["{}"]}}'.format(
                i, random.choice(categories)
            )
        )
    return body


@ingest_router.post("/news")
async def ingest_raw_news(
    db: DBDependency,
    service_account: Annotated[
        ServiceAccountSchema, Depends(ServiceAccountAuth())
    ],
    body: List[Json[Any]] = Body(example=generate_fake_ingest_body()),
):
    logger.info(f"Ingesting raw news data {body}")

    raw_news_service = RawNewsService()
    results = await raw_news_service.create_raw_news_bulk(
        db=db, service_account_id=service_account.id, raw_news_data_values=body
    )

    await get_pub_sub_logging_service().log(
        "news", f"Пришло {len(results)} сырых новостей на обработку"
    )
    for raw_news in results:
        process_raw_news.delay(raw_news.id)

    return Response(status_code=HTTP_200_OK)
