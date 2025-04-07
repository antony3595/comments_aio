from contextlib import asynccontextmanager
from typing import List

import config
from clients.base import BaseAsyncHttpClient
from config import logging
from schema.json_placeholder import Post, Comment, PostPatchDTO

logger = logging.getLogger(__name__)


class JsonPlaceholderClient(BaseAsyncHttpClient):

    async def get_posts(self, **kwargs) -> List[Post]:
        url = "/posts"
        method = "GET"
        response = await self._make_request(method, url, **kwargs)
        response_json = await response.json()

        posts = [Post(**post_dict) for post_dict in response_json]

        return posts

    async def get_post_comments(self, post_id: int, **kwargs) -> List[Comment]:
        url = "/comments"
        method = "GET"
        params = {"postId": post_id}
        response = await self._make_request(
            method, url, params=params, **kwargs
        )
        response_json = await response.json()
        comments = [Comment(**comment_dict) for comment_dict in response_json]
        return comments

    async def partially_update_post(
        self, post: PostPatchDTO, **kwargs
    ) -> PostPatchDTO:
        url = f"/posts/{post.id}"
        method = "PATCH"
        response = await self._make_request(
            method, url, data=post.model_dump(exclude_unset=True), **kwargs
        )
        response_json = await response.json()
        updated_post = PostPatchDTO(**response_json)
        return updated_post


@asynccontextmanager
async def get_json_placeholder_client() -> JsonPlaceholderClient:
    async with JsonPlaceholderClient(
        base_url=config.settings.BLOGS_API_URL
    ) as client:
        yield client
