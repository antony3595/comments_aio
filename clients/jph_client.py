from typing import List

from aiohttp import ClientSession

import conf
from clients.base import BaseHttpClient
from conf import logging
from schema.json_placeholder import Post, Comment, PostPatchDTO

logger = logging.getLogger(__name__)


class JsonPlaceholderClient(BaseHttpClient):
    API_URL = conf.settings.BLOGS_API_URL

    async def get_posts(self, session: ClientSession, **kwargs) -> List[Post]:
        url = f"{self.API_URL}/posts"
        method = "GET"
        response = await self._make_request(session, method, url, **kwargs)
        response_json = await response.json()

        posts = [Post(**post_dict) for post_dict in response_json]

        return posts

    async def get_post_comments(self, post_id: int, session: ClientSession, **kwargs) -> List[Comment]:
        url = f"{self.API_URL}/comments"
        method = "GET"
        params = {"postId": post_id}
        response = await self._make_request(session, method, url, params=params, **kwargs)
        response_json = await response.json()
        comments = [Comment(**comment_dict) for comment_dict in response_json]
        return comments

    async def partially_update_post(self, post: PostPatchDTO, session: ClientSession, **kwargs) -> PostPatchDTO:
        url = f"{self.API_URL}/posts/{post.id}"
        method = "PATCH"
        response = await self._make_request(session, method, url, data=post.model_dump(exclude_unset=True), **kwargs)
        response_json = await response.json()
        updated_post = PostPatchDTO(**response_json)
        return updated_post
