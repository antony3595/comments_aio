import logging
from uuid import uuid4

import aiohttp
from aiohttp import ClientResponse

logger = logging.getLogger(__name__)


class BaseHttpClient:
    def dict_to_qs(self, params: dict) -> str:
        if params:
            return "?" + "&".join([f"{key}={str(value)}" for key, value in params.items()])
        return ""

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
