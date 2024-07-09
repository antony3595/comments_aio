import asyncio
import json
import logging

import aiohttp

import conf
from clients.json_placeholder_client.client import JsonPlaceholderClient

logger = logging.getLogger(__name__)


def validate_data(data: dict):
    assert isinstance(data, dict) and data.get("id"), "Invalid data"


async def update_data(validated_data: dict):
    async with aiohttp.ClientSession() as session:
        client = JsonPlaceholderClient()
        post_id = validated_data["postId"]
        response_data = await client.partially_update_post(post_id, {"title": "foo"}, session)
        return response_data


async def handle_request(reader, writer):
    data = await reader.read(1000)
    message = data.decode()
    parsed_data = json.loads(message)
    logger.info(f"Server got message: {message}")

    try:
        validate_data(parsed_data)

        updated_data = await update_data(parsed_data)
        writer.write(json.dumps(updated_data).encode())
        await writer.drain()
        logger.info(f"Server responded with {data}")

    except Exception as e:
        logger.error(repr(e))
    finally:
        writer.close()
        logger.info(f"Server closing connection")
        await writer.wait_closed()


async def main():
    logger.info(f"Running server on {conf.TCP_SERVER_HOST}:{conf.TCP_SERVER_PORT}")

    server = await asyncio.start_server(
        handle_request, conf.TCP_SERVER_HOST, conf.TCP_SERVER_PORT)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
