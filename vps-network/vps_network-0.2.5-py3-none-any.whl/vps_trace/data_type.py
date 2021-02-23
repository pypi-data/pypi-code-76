from typing import Optional, List

from pydantic import Field, BaseModel

__all__ = ["TraceHop", "TraceResult"]


class TraceHop(BaseModel):
    """
    注意: 在 Traceroute 有可能在跟踪的时候 IP 地址也会发生变化
    但是我们并不考虑这个问题，要不然有可能导致后面没有办法画图
    也可以使用 fast 模式来避免这个问题。
    """

    ip: str = Field(..., title="IP地址")
    # rtt times
    times: List[Optional[float]] = Field(..., title="RTT时间", description="没有则表示没有收到回复")
    # any other ip information
    info: Optional[dict] = Field(None, title="其他信息")


class TraceResult(BaseModel):
    results: List[Optional[TraceHop]] = Field(..., title="Trace结果")
