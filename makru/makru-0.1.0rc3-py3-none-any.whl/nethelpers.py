from typing import Iterable, List, Optional
from clint.textui import progress
from httpx import AsyncClient, ConnectError, ConnectTimeout
from dataclasses import dataclass
from time import perf_counter
import asyncio
from asyncio import Future

@dataclass
class DownloadRequest(object):
    url: str
    dest: str
    tried: int = 0

    @property
    def retried(self):
        if self.tried == 0:
            return 0
        else:
            return self.tried - 1

@dataclass
class DownloadResult(object):
    done: bool
    request: DownloadRequest
    http_status_code: int
    bytes_recv: int
    exception: Optional[BaseException] = None

@dataclass
class ProgressCalculatorUnit(object):
    request: DownloadRequest
    required: float = 0
    current: float = 0
    completed: bool = False
    speed: Optional[float] = None

    @property
    def self_progress(self) -> float:
        if self.completed:
            return 1
        if self.required <= 0 or self.current <= 0:
            return 0
        return self.current / self.required

class ProgressCalculator(object):
    def __init__(self, requests: List[DownloadRequest]) -> None:
        self.requests: List[DownloadRequest] = requests
        self.units: List[ProgressCalculatorUnit] = list(map(ProgressCalculatorUnit, requests))
        self.avg_unit_progress = 1 / len(requests)
    
    def get_unit(self, request: DownloadRequest):
        return self.units[self.requests.index(request)]
    
    def progress(self) -> float:
        current_prgress = 0.0
        for unit in self.units:
            unit_progress = unit.self_progress * self.avg_unit_progress
            current_prgress += unit_progress
        return current_prgress
    
    def speed(self) -> float:
        total_speed = 0.0
        for unit in self.units:
            if unit.speed:
                total_speed += unit.speed
        return total_speed

async def _stream_request(client: AsyncClient, request: DownloadRequest, progress_calculator: ProgressCalculator) -> DownloadResult:
    unit = progress_calculator.get_unit(request)
    request.tried += 1
    async with client.stream('GET', request.url) as stream:
        with open(request.dest, mode='wb+') as file:
            if stream.status_code == 200:
                try:
                    length_list = stream.headers.get_list('Content-Length')
                    length = None
                    if len(length_list) > 0:
                        length_s = length_list[-1]
                        try:
                            length = int(length_s)
                        except ValueError:
                            pass
                    if length:
                        unit.required = length
                    async for b in stream.aiter_bytes():
                        start_time = perf_counter()
                        block_length = len(b)
                        file.write(b)
                        unit.current += block_length
                        end_time = perf_counter()
                        delta = end_time - start_time
                        unit.speed = block_length / delta
                    if length and length == unit.current:
                        unit.completed = True
                    elif not length:
                        unit.completed = True
                except Exception as e:
                    return DownloadResult(done=False, request=request, http_status_code=stream.status_code, bytes_recv=-1, exception=e)
        return DownloadResult(done=unit.completed, request=request, http_status_code=stream.status_code, bytes_recv=unit.current)

def _human_size_string(bytes_size: float):
    aByte = 1
    aKByte = 1024 * aByte
    aMByte = 1024 * aKByte
    aGByte = 1024 * aMByte
    if bytes_size <= aKByte:
        return "{} Bytes".format(bytes_size)
    elif bytes_size <= aMByte:
        return "{} KBytes".format(bytes_size / aKByte)
    elif bytes_size <= aGByte:
        return "{} MBytes".format(bytes_size / aMByte)
    else:
        return "{} GBytes".format(bytes_size / aGByte)

async def _progress_bar(label: str, progress_calc: ProgressCalculator):
    with progress.Bar(label=label, expected_size=len(label)) as bar:
        while True:
            bar.show(progress_calc.progress())
            bar.label = "{}/s".format(_human_size_string(progress_calc.speed()))
            await asyncio.sleep(1)

async def download_batch_async(requests: List[DownloadRequest], max_retried: int = 3, show_progress: bool = False) -> List[DownloadResult]:
    progress_calc = ProgressCalculator(requests)
    requests_queue: List[DownloadRequest] = []
    requests_queue.extend(requests)
    results: List[DownloadResult] = []
    show_progress_future = None
    if show_progress:
        show_progress_future = asyncio.ensure_future(_progress_bar("Downloading...", progress_calc))
    async with AsyncClient() as client:
        while len(requests_queue) > 0:
            futures: List[Future[DownloadResult]] = []
            for request in requests_queue:
                futures.append(asyncio.ensure_future(_stream_request(client, request, progress_calc)))
            requests_queue = []
            for f in asyncio.as_completed(futures):
                download_result = await f
                if download_result.exception:
                    if download_result.request.retried <= max_retried:
                        requests_queue.append(download_result.request)
                    else:
                        results.append(download_result)
                elif download_result.http_status_code >= 500 and download_result.http_status_code <= 599:
                    requests_queue.append(download_result.request)
                else:
                    results.append(download_result)
    if show_progress_future:
        show_progress_future.cancel()
    return results

async def download_async(url: str, dest: str, max_retried: int = 3, show_progress: bool = False):
    return (await download_batch_async(
        [DownloadRequest(url, dest)],
        max_retried = max_retried,
        show_progress = show_progress,
    ))[0]

def download_batch(requests: List[DownloadRequest], max_retried: int = 3, show_progress: bool = False):
    return asyncio.run(download_batch_async(requests, max_retried, show_progress))

def download(url: str, dest: str, max_retried: int = 3, show_progress: bool = False):
    return asyncio.run(download_async(url, dest, max_retried, show_progress))

async def check_network_async(remote: str="http://captive.apple.com/generate_204") -> bool:
    """
    Check network connection to `remote`, the `remote` is expected to be a HTTP URI accepts GET method.
    This function return `True` when the access to `remote` replied 200-299 as status code.
    """
    try:
        async with AsyncClient() as client:
            response = await client.get(remote)
            return response.status_code >= 200 or response.status_code <= 299
    except ConnectError:
        return False
    except ConnectTimeout:
        return False

def check_network(remote: str="http://captive.apple.com/generate_204", timeout: float=3) -> bool:
    """
    This function is synchronous version of `check_network_async`.
    If the remote does not respond after `timeout` second(s), the function return `False`.
    """
    try:
        return asyncio.run(asyncio.wait_for(check_network_async(remote), timeout))
    except asyncio.TimeoutError:
        return False
