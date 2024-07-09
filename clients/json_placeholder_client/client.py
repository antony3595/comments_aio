from uuid import uuid4

import aiohttp
from aiohttp import ClientSession, ClientResponse

import conf
from conf import logging

logger = logging.getLogger(__name__)


class JsonPlaceholderClient:
    API_URL = conf.BLOGS_API_URL

    def dict_to_qs(self, params: dict) -> str:
        if params:
            return "?" + "&".join([f"{key}={str(value)}" for key, value in params.items()])
        return ""

    # TODO move method to BaseClient
    async def _make_request(self, session, method, url, **kwargs) -> ClientResponse:
        request_uuid = uuid4().hex
        params_str = self.dict_to_qs(kwargs.get("params", {}))
        url_with_search_params = url + params_str

        logger.info(f"Sending request {method}:{url_with_search_params}, request_uuid={request_uuid}")

        try:
            response = await session.request(method=method, url=url, **kwargs)
            response.raise_for_status()
            logger.info(f"Got response with code {response.status} from {method}:{response.real_url}, uuid={request_uuid}")
            return response
        except (
                aiohttp.ClientError,
                aiohttp.http_exceptions.HttpProcessingError,
        ) as e:
            logger.error(
                "aiohttp exception for %s [%s]: %s",
                url_with_search_params,
                getattr(e, "status", None),
                getattr(e, "message", None),
            )
            raise e

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
