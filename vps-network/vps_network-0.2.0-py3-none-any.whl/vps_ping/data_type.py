from typing import List, Optional

from pydantic import BaseModel, Field

__all__ = ["PingResult"]


class PingResult(BaseModel):
    host: str = Field(..., title="目的服务器", description="从本机Ping的目的服务器")
    times: List[Optional[float]] = Field(
        ...,
        title="RTT时间",
        description="rtt(round trip time)列表, 如果没有数据: rtt = None 注意: 时间单位为 ms",
    )

    def __str__(self) -> str:
        return f"<PingResult Host: {self.host} Times: {self.times}>"
