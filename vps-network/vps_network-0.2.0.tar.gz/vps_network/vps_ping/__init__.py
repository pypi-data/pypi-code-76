import os
from typing import List, Optional

import click

from .data_type import PingResult
from .do_multi_ping import do_multi_ping
from .print_utils import print_ping_results
from ..values import SERVER_URL

__all__ = ["init_ping_cli", "PingResult", "do_multi_ping"]


def init_ping_cli(main: click.Group):
    @main.group()
    def ping():
        """
        ping 测试
        """
        pass

    assert isinstance(ping, click.Group)

    @ping.command()
    @click.argument("host")
    @click.option("--no-telemetry", is_flag=True, help="关闭遥测数据", hidden=True)
    def single(host: str, no_telemetry: bool):
        """
        ping 目标服务器

        例如: single www.baidu.com
        """
        results = do_multi_ping([host])
        print_ping_results(results)

    @ping.command()
    @click.option("--host", multiple=True, help="目的服务器IP, 允许多个值")
    @click.option("--no-telemetry", is_flag=True, help="关闭遥测数据", hidden=True)
    def multi(host: List[str], no_telemetry: bool):
        """
        ping 多个服务器

        例如: multi --host www.baidu.com --host www.google.com
        """
        results = do_multi_ping(host)
        print_ping_results(results)

    @ping.command()
    @click.option(
        "--app-key",
        type=str,
        help="上报数据使用的 APP Key",
        default=lambda: os.getenv("VPS_NETWORK_APP_KEY", None),
    )
    @click.option("--server-url", type=str, help="服务器的URL", default=SERVER_URL)
    @click.option("--no-telemetry", is_flag=True, help="关闭遥测数据", hidden=True)
    def quick(app_key: Optional[str], server_url: str, no_telemetry: bool):
        """
        基准测试 ping 快速测试

        app key 也可以从环境变量中读取: VPS_NETWORK_APP_KEY
        """
        print(f"{app_key=} {server_url=} {no_telemetry=}")
