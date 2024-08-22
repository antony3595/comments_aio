import logging

from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.dependencies.auth import ApiKeyAuth
from api.routers import auth_router, news_router

logger = logging.getLogger(__name__)

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors(), "body": exc.body},
    )


@app.get("/", dependencies=[Depends(ApiKeyAuth)])
async def root():
    return {"message": "Hello World"}


app.include_router(auth_router)
app.include_router(news_router)
