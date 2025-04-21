import logging
import time
from pprint import pprint

from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.dependencies.auth import ApiKeyAuth
from api.routers import auth_router, news_router, ingest_router
from config import settings
from schema.api.logs import PubSubLogMessage
from services.pubsub_logging.service import get_pub_sub_logging_service

logger = logging.getLogger(__name__)

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors(), "body": exc.body},
    )


@app.middleware("http")
async def log_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start
    log_service = get_pub_sub_logging_service()

    message = PubSubLogMessage(
        headers=dict(request.headers),
        method=request.method,
        path=request.url.path,
        params=dict(request.query_params),
        code=response.status_code,
        process_time=process_time,
    )

    await log_service.log(
        "http",
        message=message.model_dump_json(),
    )

    return response


@app.get("/", dependencies=[Depends(ApiKeyAuth)])
async def root():
    return {"message": "Hello World"}


app.include_router(auth_router)
app.include_router(news_router)
app.include_router(ingest_router)

pprint(settings.model_dump())
