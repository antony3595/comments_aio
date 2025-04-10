from typing import Any

from pydantic import BaseModel


class PubSubLogMessage(BaseModel):
    headers: dict[str, str]
    method: str
    path: str
    params: dict[str, Any]
    code: int | None = None
    process_time: float | None = None
