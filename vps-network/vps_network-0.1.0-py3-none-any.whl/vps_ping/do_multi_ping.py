from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import List, Optional

from icmplib import (
    PID,
    resolve,
    is_ipv6_address,
    ICMPv4Socket,
    ICMPv6Socket,
    ICMPRequest,
    ICMPLibError,
)
from pydantic import BaseModel, Field
from rich.progress import Progress, BarColumn, TimeRemainingColumn

__all__ = ["do_multi_ping", "PingResult"]


class PingResult(BaseModel):
    host: str = Field(..., title="host")
    times: List[Optional[float]] = Field(
        ...,
        title="时间",
        description="rtt(round trip time)列表, 如果没有数据: rtt = None 注意: 时间单位为 ms",
    )

    def __str__(self) -> str:
        return f"<PingResult Host: {self.host} Times: {self.times}>"


def do_one_ping(
    host,
    progress: Progress,
    seq_offset=0,
    count=8,
    interval=0.1,
    timeout=2,
    id=PID,
    source=None,
    **kwargs,
) -> PingResult:
    """
    :raises NameLookupError: If you pass a hostname or FQDN in
        parameters and it does not exist or cannot be resolved.
    :raises SocketPermissionError: If the privileges are insufficient
        to create the socket.
    :raises SocketAddressError: If the source address cannot be
        assigned to the socket.
    :raises ICMPSocketError: If another error occurs. See the
        `ICMPv4Socket` or `ICMPv6Socket` class for details.
    """

    task_id = progress.add_task(host, total=count)

    address = resolve(host)

    # on linux `privileged` must be True
    if is_ipv6_address(address):
        sock = ICMPv6Socket(address=source, privileged=True)
    else:
        sock = ICMPv4Socket(address=source, privileged=True)

    times = []

    for sequence in range(count):
        progress.update(task_id, advance=1)

        request = ICMPRequest(
            destination=address, id=id, sequence=sequence + seq_offset, **kwargs
        )

        try:
            sock.send(request)

            reply = sock.receive(request, timeout)
            reply.raise_for_status()

            round_trip_time = (reply.time - request.time) * 1000
            times.append(round_trip_time)

            if sequence < count - 1:
                sleep(interval)

        except ICMPLibError:
            times.append(None)

    sock.close()

    return PingResult(host=address, times=times)


def do_multi_ping(
    hosts: List[str], count: int = 8, interval: float = 0.01, timeout: int = 2
) -> List[PingResult]:
    pool = ThreadPoolExecutor(max_workers=len(hosts), thread_name_prefix="ping")

    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "{task.completed} / {task.total}",
        TimeRemainingColumn(),
        transient=True,
    ) as progress:
        jobs = []
        for idx in range(len(hosts)):
            job = pool.submit(
                do_one_ping,
                seq_offset=idx * len(hosts) * 2,
                host=hosts[idx],
                count=count,
                interval=interval,
                timeout=timeout,
                progress=progress,
            )
            jobs.append(job)

        results: List[PingResult] = list(map(lambda x: x.result(), jobs))

    return results
