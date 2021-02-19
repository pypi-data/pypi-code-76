from time import sleep
from typing import List, Optional

from icmplib import (
    PID,
    Hop,
    resolve,
    is_ipv6_address,
    ICMPv4Socket,
    ICMPv6Socket,
    ICMPRequest,
    TimeExceeded,
    ICMPLibError,
    ICMPReply,
)
from rich.table import Table

from .ip_api import get_ip_info

__all__ = ["do_traceroute"]


def do_traceroute(
    table: Table,
    address: str,
    count: int = 2,
    interval: float = 0.05,
    timeout: int = 3,
    id: int = PID,
    first_hop: int = 1,
    max_hops: int = 32,
    source: Optional[str] = None,
    fast: bool = False,
    **kwargs,
) -> List[Hop]:
    """
    :param table: rich 动态表格

    参数的含义与: `icmplib.traceroute` 保持一致
    """
    address = resolve(address)

    if is_ipv6_address(address):
        sock = ICMPv6Socket(source)
    else:
        sock = ICMPv4Socket(source)

    ttl = first_hop
    host_reached = False
    hops = []

    while not host_reached and ttl <= max_hops:
        hop_address = None
        packets_sent = 0
        packets_received = 0

        min_rtt = float("inf")
        avg_rtt = 0.0
        max_rtt = 0.0

        for sequence in range(count):
            request = ICMPRequest(
                destination=address, id=id, sequence=sequence, ttl=ttl, **kwargs
            )

            reply: Optional[ICMPReply] = None
            try:
                sock.send(request)
                packets_sent += 1

                reply = sock.receive(request, timeout)
                reply.raise_for_status()
                host_reached = True

            except TimeExceeded:
                sleep(interval)

            except ICMPLibError:
                continue

            assert reply is not None

            hop_address = reply.source
            packets_received += 1

            round_trip_time = (reply.time - request.time) * 1000
            avg_rtt += round_trip_time
            min_rtt = min(round_trip_time, min_rtt)
            max_rtt = max(round_trip_time, max_rtt)

            if fast:
                break

        if packets_received:
            avg_rtt /= packets_received

            hop = Hop(
                address=hop_address,
                min_rtt=min_rtt,
                avg_rtt=avg_rtt,
                max_rtt=max_rtt,
                packets_sent=packets_sent,
                packets_received=packets_received,
                distance=ttl,
            )

            hops.append(hop)
            ip_info = get_ip_info(hop.address)
            if ip_info is None:
                position = ""
                isp = ""
            else:
                position = f"{ip_info.country} {ip_info.regionName} {ip_info.city}"
                isp = f"{ip_info.isp}"
            table.add_row(
                f"{hop.address}",  # 地址
                position,  # 位置
                isp,  # ISP
                f"{hop.min_rtt:.2f}",  # min
                f"{hop.avg_rtt:.2f}",  # avg
                f"{hop.max_rtt:.2f}",  # max
            )
        else:
            table.add_row("*", "*", "*", "*", "*", "*")

        ttl += 1

    sock.close()

    return hops
