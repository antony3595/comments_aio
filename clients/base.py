import logging
from uuid import uuid4
from urllib.parse import urlencode
import aiohttp
from aiohttp import ClientResponse

logger = logging.getLogger(__name__)


class BaseAsyncHttpClient:

    def __init__(self, *args, **kwargs):
        self.session = aiohttp.ClientSession(*args, **kwargs)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def _make_request(self, method, url, **kwargs) -> ClientResponse:
        request_uuid = uuid4().hex

        params_str = urlencode(kwargs.get("params", {}))
        url_with_search_params = str(self.base_url) + url + "?" + params_str
        logger.info(f"Sending request {method}:{url_with_search_params}, request_uuid={request_uuid}")

        try:
            response = await self.session.request(method=method, url=url, **kwargs)
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

    @property
    def base_url(self) -> str:
        return self.session._base_url
