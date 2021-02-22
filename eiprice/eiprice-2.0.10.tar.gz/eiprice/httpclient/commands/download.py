# import asyncio
from typing import List

# import nest_asyncio

from eiprice.httpclient.adapters.asynchronous import gather_with_concurrency
from eiprice.httpclient.adapters.specs.http import DownloadSpec
from eiprice.httpclient.commands.action import Action
# from httpclient.core.asynchronous import RequestAsyncDownloader
from eiprice.httpclient.core.synchronous import RequestSyncDownloader

# nest_asyncio.apply()


# def exec_async_coroutine(coroutines):
#     loop = asyncio.get_event_loop()
#     result = loop.run_until_complete(coroutines)

#     return result


class SyncDownloadSingleURL(Action):
    def __init__(self, spec: DownloadSpec):
        self.spec = spec
        self.downloader = RequestSyncDownloader()

    def execute(self):
        return self.downloader.execute(
            self.spec.method.value,
            self.spec.url,
            headers=self.spec.headers,
            params=self.spec.params,
            json=self.spec.json,
            payload=self.spec.data,
            proxies=self.spec.proxies,
            cookies=self.spec.cookies,
            verify=self.spec.verify,
            timeout=self.spec.timeout,

        )


# class AsyncDownloadSingleURL(Action):
#     def __init__(self, spec: DownloadSpec):
#         self.spec = spec
#         self.downloader = RequestAsyncDownloader()

#     def execute(self):
#         result = exec_async_coroutine(
#             self.downloader.execute(
#                 self.spec.method.value,
#                 self.spec.url,
#                 headers=self.spec.headers,
#                 params=self.spec.params,
#                 json=self.spec.json,
#                 payload=self.spec.data,
#                 proxies=self.spec.proxies,
#             )
#         )

#         return result


# class AsyncDownloadManyURLS(Action):
#     def __init__(self, specs: List[DownloadSpec], max_workers: int = 5):
#         self.specs = specs
#         self.max_workers = max_workers
#         self.downloader = RequestAsyncDownloader()

#     def execute(self):
#         result = exec_async_coroutine(
#             gather_with_concurrency(
#                 self.max_workers,
#                 *[
#                     self.downloader.execute(
#                         spec.method.value,
#                         spec.url,
#                         headers=spec.headers,
#                         params=spec.params,
#                         json=spec.json,
#                         payload=spec.data,
#                         proxies=spec.proxies,
#                         time_between_requests=spec.time_between_requests,
#                     )
#                     for spec in self.specs
#                 ]
#             )
#         )

#         return result
