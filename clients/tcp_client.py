import asyncio
import logging

import conf
from schema.json_placeholder import Comment, Post
from schema.tcp_server import ClientCommentRequestDTO

logger = logging.getLogger(__name__)


class TCPConnection:
    async def __aenter__(self):
        logger.info(f"Opening TCP connection {conf.settings.TCP_SERVER_HOST}:{conf.settings.TCP_SERVER_PORT}")

        reader, writer = await asyncio.open_connection(conf.settings.TCP_SERVER_HOST, conf.settings.TCP_SERVER_PORT)

        self.reader = reader
        self.writer = writer
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.writer.close()
        logger.info(f"Closing TCP connection {conf.settings.TCP_SERVER_HOST}:{conf.settings.TCP_SERVER_PORT}")
        await self.writer.wait_closed()


class TCPServerClient:
    async def update_post_by_comment(self, comment: Comment) -> Post:
        dto = ClientCommentRequestDTO(**comment.model_dump(include={'postId', 'id', 'email'}))

        async with TCPConnection() as conn:
            conn.writer.write(dto.model_dump_json().encode())
            await conn.writer.drain()

            response = await conn.reader.read(1000)
            decoded = response.decode()
            logger.info(f"Server responded with: {response}")
            post = Post.model_validate_json(decoded)
            return post
