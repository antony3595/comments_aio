import logging

from fastapi import FastAPI, Depends

from api.dependencies.auth import ApiKeyAuth
from api.routers import auth_router, news_router

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/", dependencies=[Depends(ApiKeyAuth)])
async def root():
    return {"message": "Hello World"}


app.include_router(auth_router)
app.include_router(news_router)
