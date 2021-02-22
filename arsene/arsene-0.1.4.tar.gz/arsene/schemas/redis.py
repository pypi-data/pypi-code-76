from typing import Any, Optional
from pydantic import BaseModel


class RedisModel(BaseModel):
    host: str
    port: int = 6379
    db: Any = 0
    password: Optional[str] = None
    socket_connect_timeout: int = 1

    class Config:
        orm_mode = True
