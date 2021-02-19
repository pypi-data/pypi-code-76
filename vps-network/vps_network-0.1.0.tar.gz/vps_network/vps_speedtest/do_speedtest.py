"""
这个脚本包装了 Speed Test Cli
github: https://github.com/sivel/speedtest-cli/wiki

之后应该迁移到自建的 SpeedTest 工具上
"""

from typing import Optional, Any

from pydantic import BaseModel, Field
from rich.progress import Progress, BarColumn, TimeElapsedColumn, TaskID
from speedtest import Speedtest

__all__ = ["do_speed_test", "SpeedTestResult"]


class SpeedTestServer(BaseModel):
    url: str = Field(..., title="网页地址")
    lat: str = Field(..., title="经度")
    lon: str = Field(..., title="纬度")
    name: str = Field(..., title="名称")
    country: str = Field(..., title="国家")
    cc: str = Field(..., title="")
    sponsor: str = Field(..., title="贡献者")
    id: str = Field(..., title="服务器ID")
    host: str = Field(..., title="服务器地址")
    d: float = Field(..., title="")
    latency: float = Field(..., title="延迟")


class SpeedTestClient(BaseModel):
    ip: str = Field(..., title="")
    lat: str = Field(..., title="经度")
    lon: str = Field(..., title="纬度")
    isp: str = Field(..., title="ISP 提供商")
    isprating: str = Field(..., title="")
    rating: str = Field(..., title="")
    ispdlavg: str = Field(..., title="")
    ispulavg: str = Field(..., title="")
    loggedin: str = Field(..., title="")
    country: str = Field(..., title="")


class SpeedTestResult(BaseModel):
    download: float = Field(..., title="下载速度")
    upload: float = Field(..., title="上传速度")
    ping: float = Field(..., title="ping")
    server: SpeedTestServer = Field(..., title="服务器")
    timestamp: str = Field(..., title="时间")
    bytes_sent: Optional[int] = Field(None, title="发送字节")
    bytes_received: Optional[int] = Field(None, title="接受字节")
    share: Optional[Any] = Field(None, title="分享")
    client: SpeedTestClient = Field(..., title="客户端信息")


def speed_test_cb(progress: Progress, task_id: TaskID, idx: int, total: int, **kwargs):
    if kwargs.get("end") is True:
        progress.update(task_id, total=total, completed=idx + 1)


def do_speed_test(
    server: Optional[str] = None,
    disable: Optional[str] = None,
    up_threads: Optional[int] = None,
    dl_threads: Optional[int] = None,
) -> SpeedTestResult:
    """
    进行 SpeedTest 测试

    服务器列表 ID 可以从这儿获取: https://williamyaps.github.io/wlmjavascript/servercli.html

    每次仅允许测试一个服务器

    :param server: 期望的服务器ID (ID 来自于 SpeedTest 官网)
    :param disable: up|down 禁止测试 上传/下载
    :param up_threads: 上传线程数量
    :param dl_threads: 下载线程数量
    """
    st = Speedtest()

    st.get_servers(servers=None if server is None else [server])

    server = st.best

    if disable != "up":
        with Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "{task.completed} / {task.total}",
            TimeElapsedColumn(),
        ) as progress:
            task_id = progress.add_task(f"上传: {server['host']}")

            def up_cb(idx, total, **kwargs):
                speed_test_cb(progress, task_id, idx, total, **kwargs)

            st.upload(threads=up_threads, callback=up_cb)
    if disable != "dl":
        with Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "{task.completed} / {task.total}",
            TimeElapsedColumn(),
        ) as progress:
            task_id = progress.add_task(f"下载: {server['host']}")

            def dl_cb(idx, total, **kwargs):
                speed_test_cb(progress, task_id, idx, total, **kwargs)

            st.download(threads=dl_threads, callback=dl_cb)

    return SpeedTestResult(**st.results.dict())
