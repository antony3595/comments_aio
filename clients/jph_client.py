from aiohttp import ClientSession

import conf
from clients.base import BaseHttpClient
from conf import logging

logger = logging.getLogger(__name__)


class JsonPlaceholderClient(BaseHttpClient):
    API_URL = conf.BLOGS_API_URL

    async def get_posts(self, session: ClientSession, **kwargs):
        url = f"{self.API_URL}/posts"
        method = "GET"
        response = await self._make_request(session, method, url, **kwargs)

        return await response.json()

    async def get_post_comments(self, post_id: int, session: ClientSession, **kwargs):
        url = f"{self.API_URL}/comments"
        method = "GET"
        params = {"postId": post_id}
        response = await self._make_request(session, method, url, params=params, **kwargs)

        return await response.json()

    async def partially_update_post(self, post_id: int, data: dict, session: ClientSession, **kwargs):
        url = f"{self.API_URL}/posts/{post_id}"
        method = "PATCH"
        response = await self._make_request(session, method, url, data=data, **kwargs)

        return await response.json()
