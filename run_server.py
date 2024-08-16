import asyncio
import logging

import aiohttp
from pydantic import ValidationError

import conf
from schema.json_placeholder import PostPatchDTO
from schema.tcp_server import ServerCommentRequestDTO
from clients.jph_client import JsonPlaceholderClient, get_json_placeholder_client

logger = logging.getLogger(__name__)


async def update_post_by_comment(post: ServerCommentRequestDTO) -> PostPatchDTO:
    async with get_json_placeholder_client() as client:
        post_patch_dto = PostPatchDTO.model_validate({"id": post.postId})
        post_patch_dto.title = "Updated post title"
        response_data = await client.partially_update_post(post_patch_dto)
        return response_data


async def handle_request(reader, writer):
    data = await reader.read(1000)
    message = data.decode()

    logger.info(f"Server got message: {message}")

    try:
        post = ServerCommentRequestDTO.model_validate_json(data)
        updated_data = await update_post_by_comment(post)
        logger.info(f"Responding with message {updated_data.model_dump_json()}")
        writer.write(updated_data.model_dump_json().encode())

    except ValidationError as e:
        logger.error(e.json())
        writer.write(e.json().encode())

    except Exception as e:
        logger.error(repr(e).encode())
        writer.write(repr(e).encode())

    finally:
        await writer.drain()
        writer.close()
        logger.info(f"Server closing connection")
        await writer.wait_closed()


async def main():
    logger.info(f"Running server on {conf.settings.TCP_SERVER_HOST}:{conf.settings.TCP_SERVER_PORT}")

    server = await asyncio.start_server(
        handle_request, conf.settings.TCP_SERVER_HOST, conf.settings.TCP_SERVER_PORT)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
