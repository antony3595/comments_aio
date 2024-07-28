import asyncio
import json
import logging

import conf

logger = logging.getLogger(__name__)


class TCPConnection:
    async def __aenter__(self):
        logger.info(f"Opening TCP connection {conf.TCP_SERVER_HOST}:{conf.TCP_SERVER_PORT}")

        reader, writer = await asyncio.open_connection(conf.TCP_SERVER_HOST, conf.TCP_SERVER_PORT)

        self.reader = reader
        self.writer = writer
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.writer.close()
        logger.info(f"Closing TCP connection {conf.TCP_SERVER_HOST}:{conf.TCP_SERVER_PORT}")
        await self.writer.wait_closed()


class TCPServerClient:
    async def update_comment(self, data: dict):
        async with TCPConnection() as conn:
            conn.writer.write(json.dumps(data).encode())
            await conn.writer.drain()

            response = await conn.reader.read(1000)
            decoded = response.decode()
            logger.info(f"Server responded with: {response}")
            return decoded
