"""
快速测试 ping, traceroute, speed
"""

import logging
import os
import sys
from typing import Optional, List

import click
from rich.logging import RichHandler

from ..vps_api import NetworkApi
from ..vps_api.dt import ServerListForm, PingForm, TraceForm, SpeedForm
from ..vps_ping import do_multi_ping
from ..vps_speed import do_speed_test_wrap
from ..vps_trace import TraceResult, do_traceroute_v2_wrapper

__all__ = ["init_quick_cli"]


def init_quick_cli(main: click.Group):
    @main.command()
    @click.option(
        "--app-key",
        type=str,
        required=True,
        help="上报数据的APPKey",
        default=lambda: os.environ.get("VPS_APP_KEY", "").strip(),
        show_default="VPS_APP_KEY",
    )
    @click.option(
        "--job-id",
        type=str,
        help="测试任务的ID",
        default=lambda: os.environ.get("VPS_JOB_ID", None),
    )
    @click.option("--cc", type=str, help="测试目标国家,没有设置则随机选择")
    @click.option("--limit", type=int, help="要测试多少个服务器")
    @click.option("--ping-count", type=int, help="Ping 测试发送数据包的数量", default=8)
    @click.option("--trace-hops", type=int, help="Traceroute 最大跳", default=32)
    @click.option("--trace-count", type=int, help="Traceroute 发送数据包的数量", default=2)
    @click.option(
        "--interval", type=float, help="Ping/Trace 测试发送数据包的间隔时间", default=0.05
    )
    @click.option("--timeout", type=int, help="Ping/Trace 测试超时时间", default=3)
    @click.option(
        "--speed-disable",
        type=click.Choice(["up", "dl"], case_sensitive=False),
        help="禁止 上传/下载 测试, 不允许同时禁止",
    )
    def quick(
        app_key: str,
        job_id: Optional[str],
        cc: Optional[str],
        limit: Optional[int],
        ping_count: int,
        trace_hops: int,
        trace_count: int,
        interval: float,
        timeout: int,
        speed_disable: Optional[str],
    ):
        """
        VPS 网络快速测试
        """
        logging.basicConfig(  # noqa
            level="NOTSET",
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler()],
        )

        log = logging.getLogger("rich")
        if len(app_key) == 0:
            log.error("没有配置 app key")
            sys.exit(2)

        job_id = None if job_id in ("", None) else job_id.strip()

        api = NetworkApi(app_key)
        log.info("开始上报遥测数据")
        api.telemetry()

        # get server list
        form = (
            ServerListForm(cc=cc)
            if limit is None
            else ServerListForm(cc=cc, limit=limit)
        )

        log.info("开始获取服务器列表...")
        server_list = api.server_list(form)

        if len(server_list) == 0:
            log.error("获取服务器列表失败")
            sys.exit(1)

        log.info(f"获取服务器列表成功: {server_list}")

        # do ping
        hosts = []
        for item in server_list:
            hosts.append(item.host)

        log.info(f"执行 ping {hosts}....")
        ping_result = do_multi_ping(
            hosts, count=ping_count, interval=interval, timeout=timeout
        )

        ping_form = PingForm(job_id=job_id, results=ping_result)
        ret = api.ping_report(ping_form)
        if ret is not None and ret.errno == 0:
            log.info("上报 Ping 测试信息成功")
        else:
            log.error(f"上报 Ping 结果失败: {ret}")

        # do traceroute
        trace_results: List[TraceResult] = []
        for host in hosts:
            p = do_traceroute_v2_wrapper(
                address=host,
                count=trace_count,
                interval=interval,
                timeout=timeout,
                max_hops=trace_hops,
            )
            if p is None:
                continue
            trace_results.append(p)

        trace_form = TraceForm(job_id=job_id, results=trace_results)
        ret = api.trace_report(trace_form)
        if ret.errno == 0:
            log.info("上报 Traceroute 测试信息成功")
        else:
            log.error(f"上报 traceroute 结果失败: {ret}")

        # do speed test
        speed_result = []
        for item in server_list:
            if item.speed_test_id is None:
                continue

            log.info(f"速度测试: {item.name} {item.host}")
            v = do_speed_test_wrap(
                server=str(item.speed_test_id), disable=speed_disable
            )
            if v is None:
                log.error(
                    f"速度测试: {item.name}(host={item.host}, id = {item.speed_test_id}) 失败"
                )
            else:
                log.info(f"速度测试: {item.name} 已完成")
                speed_result.append(v)
        speed_form = SpeedForm(job_id=job_id, results=speed_result)
        ret = api.speed_report(speed_form)
        if ret.errno == 0:
            log.info("上报速度测试结果成功")
        else:
            log.error(f"上报速度测试结果失败: {ret}")
