import statistics
from typing import List

import click
from rich.console import Console
from rich.table import Table

from .do_multi_ping import do_multi_ping, PingResult

__all__ = ["init_ping_cli", "PingResult"]


def init_ping_cli(main: click.Group):
    @main.command()
    @click.option("--host", multiple=True, help="目的服务器IP, 允许多个值")
    @click.option("--no-telemetry", is_flag=True, help="关闭遥测数据", hidden=True)
    def ping(host: List[str], no_telemetry: bool):
        """
        ping 测试
        """

        results = do_multi_ping(host)

        table = Table(title="Ping 测试结果 (时间单位: ms)")
        table.add_column("IP", justify="right", style="cyan", no_wrap=True)
        table.add_column("最小RTT")
        table.add_column("最大RTT")
        table.add_column("平均RTT")
        table.add_column("标准差")
        table.add_column("失败", style="red")
        table.add_column("成功", style="green")

        for ret in results:
            success = list(filter(lambda x: x is not None, ret.times))
            if len(success) == 0:
                success = [0, 0]

            failure = len(list(filter(lambda x: x is None, ret.times)))
            row = [
                ret.host,
                f"{min(success):.2f}",
                f"{max(success):.2f}",
                f"{statistics.mean(success):.2f}",
                f"{statistics.stdev(success):.2f}",
                str(failure),
                str(len(ret.times) - failure),
            ]
            table.add_row(*row)

        console = Console()
        console.print(table)
