#! /usr/bin/env python

import asyncio
import os
from asyncio import CancelledError
from collections import defaultdict
from pathlib import Path
from time import time, time_ns
from typing import Any, Coroutine, List, Mapping, Optional, Sequence, Tuple, Union

import structlog
import zmq
from zmq.asyncio import Context, Socket

from kelvin.app.client import Request, Response
from kelvin.app.client.request import Emit
from kelvin.icd import make_message

from .common import peel, register_stop, wrap
from .injector import Injector

logger = structlog.get_logger("server")


class DevServer:
    def __init__(
        self,
        path_to_df: Union[str, Path],
        pub_url: str,
        loop_data: bool,
        verbose: bool,
        extract_path: Union[str, Path],
        extract_type: str,
        sub_url: str,
        topic: str = "",
        frequency: float = 1.0,
    ) -> None:
        self.input_path = path_to_df
        self.pub_url = pub_url
        self.loop = loop_data
        self.verbose = verbose
        self.extract_path = extract_path
        self.extract_type = extract_type
        self.sub_url = sub_url
        self.topic = topic
        self.frequency = frequency
        self.context = Context()
        self.pub_socket = self.make_socket("pub")
        self.sub_socket = self.make_socket("sub")

    def run(self) -> None:
        loop = asyncio.get_event_loop()
        to_dos = self.make_tasks()
        tasks = [loop.create_task(x) for x in to_dos]
        register_stop(tasks, loop)
        try:
            loop.run_forever()
        except CancelledError:
            pass

    def make_socket(self, socket_type: str) -> Socket:
        if socket_type == "pub":
            sock = self.context.socket(zmq.PUB)
            sock.bind(self.pub_url)
        elif socket_type == "sub":
            sock = self.context.socket(zmq.SUB)
            sock.bind(self.sub_url)
            sock.subscribe(f"{self.topic}|")
        else:
            raise ValueError(
                f'socket_type {socket_type!r} not supported - must be either "pub" or "sub"'
            )
        return sock

    def make_tasks(self) -> Sequence[Coroutine[None, None, None]]:
        to_dos = [self.injector_producer()]
        if self.extract_path:
            to_dos.append(self.extractor_consumer())
        return to_dos

    async def injector_producer(self) -> None:
        """Injector Producer process."""

        if self.verbose:
            logger.debug("Injecting Data")

        inj = Injector(path_to_df=self.input_path, loop_data=self.loop)
        runner = inj.run()

        while True:
            now_ns = time_ns()
            now = now_ns / 1e9
            try:
                output = next(runner)
                messages = [make_message("raw.float64", x, now_ns, value=output[x]) for x in output]
                response = Response(_={"time_of_validity": now_ns}, messages=messages)
                if self.verbose:
                    logger.debug(repr(response))
                await self.pub_socket.send(wrap(response.encode(), self.topic))
            except CancelledError:
                break
            except StopIteration:
                if inj.loop:
                    runner = Injector(path_to_df=self.input_path).run()
                else:
                    break
            except Exception:
                logger.exception("Unable to produce data")

            await asyncio.sleep(max(self.frequency - (time() - now), 0.0))

    async def extractor_consumer(self, n_cutoff: int = 10, max_steps: Optional[int] = None) -> None:
        """Extractor Consumer process."""

        vals = defaultdict(list)
        ixs = []
        i = 0
        while True:
            written = False
            i += 1
            try:
                data = await self.sub_socket.recv()
                try:
                    request = Request.decode(peel(data))
                    if not isinstance(request, Emit):
                        continue
                    if self.verbose:
                        logger.debug(repr(request))
                    tm = request._.time_of_validity
                    msgs = request.messages
                    if msgs:
                        ixs.append(tm)
                        for m in msgs:
                            vals[m._.name].append(m.dict()["value"])
                    # if finished cutoff period, write data
                    if not i % n_cutoff:
                        vals, ixs = self.write_data(vals, ixs, tm)
                        written = True
                except Exception:
                    logger.exception("Unable to consume data")
                    continue
                finally:
                    if max_steps is not None and i >= max_steps:
                        logger.info(f"Maximum number of steps reached ({max_steps})")
                        if not written:
                            vals, ixs = self.write_data(vals, ixs, tm)
                        break
            except CancelledError:
                break
            except Exception:
                logger.exception("Unable to consume data")

    def write_data(
        self,
        data: Mapping[str, list],
        index: Sequence[Any],
        time_of_val: int,
        partition_col: str = "last_timestamp",
    ) -> Tuple[defaultdict, List]:

        import pandas as pd

        index = pd.to_datetime(index, unit="ns", utc=True)
        df = pd.DataFrame(data, index=index)
        df[partition_col] = time_of_val
        df.index.name = "time"

        if self.verbose:
            logger.debug(f"Writing data to {self.extract_path} : shape {df.shape}")

        if self.extract_type == "parquet":
            from pyarrow import Table
            from pyarrow.parquet import write_to_dataset

            write_to_dataset(
                Table.from_pandas(df),
                str(self.extract_path),
                [partition_col],
                coerce_timestamps="us",
                allow_truncated_timestamps=True,
            )
        elif self.extract_type == "csv":
            if not os.path.isdir(self.extract_path):
                os.makedirs(self.extract_path)
            df.to_csv(f"{self.extract_path}/{str(time_of_val)}.csv")
        else:
            raise Exception(f"Unsupported extract type: {self.extract_type}")

        # return empty buffers for (data, index)
        return defaultdict(list), list()
