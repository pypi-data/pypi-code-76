import asyncio
from dataclasses import dataclass
from multiprocessing import Process
from typing import AsyncIterator

import aiobotocore
from aiobotocore.config import AioConfig


class TransferException(Exception):
    pass


def copy_from_s3_to_s3(
    source_bucket: str, source_key_prefix: str, dest_bucket: str, dest_key_prefix: str
) -> None:
    """Optimized copy from source to destination bucket. Copied objects will be renamed as '{dest_key_prefix}/{some_int}.parquet'.

    Assumptions: we want to copy at least several GiB of data, spread over a couple hundred keys.
    Thus, we will be bound by the S3 API response times, rather than the local CPU. Network should not be an
    issue as we'll use S3 to S3 copy APIs - no data will touch the local client.
    """
    # So far, the fastest way we've found to transfer data in such a manner boils down to:
    # * make as many concurrent calls as possible
    # * for objects larger than 500MiB, do a multipart copy

    # We're using asyncio here (we're not CPU-bound), in a separate process to avoid messing with the caller
    # state and ignore the GIL. There is almost no IPC and the total copy time is likely to take a few seconds
    # anyway, so the overhead of spawning a new Python process is acceptable.
    # We drop to direct calls to the S3 API rather than using wrappers provided by boto3, as we've found
    # that these wrappers do not maximize performance for typical datasets transfer.
    _run_threaded_async(_async_copy_from_s3_to_s3, _CopySource(source_bucket, source_key_prefix),
                        _CopyDestination(dest_bucket, dest_key_prefix),
    )
    # p.start()
    # # No explicit timeout here since we don't know in advance how long the operation should take.
    # p.join()
    # assert p.exitcode is not None
    # if p.exitcode != 0:
    #     raise TransferException(
    #         "S3 copy process exited with non-zero exit code. The copy is probably incomplete"
    #     )


MULTIPART_COPY_OBJ_SIZE_THRESHOLD_BYTES = 500 * 1024 * 1024
MULTIPART_COPY_PART_SIZE = 200 * 1024 * 1024
MAX_POOL_CONNECTIONS = 600


@dataclass
class _CopySource:
    bucket: str
    key_prefix: str


@dataclass
class _CopyDestination:
    bucket: str
    key_prefix: str


@dataclass
class _CopySourceObject:
    bucket: str
    key: str
    size_bytes: int


@dataclass
class _CopyDestinationObject:
    bucket: str
    key: str


@dataclass
class _UploadPartCopyResult:
    part_number: int
    etag: str


def _run_copy(source: _CopySource, destination: _CopyDestination):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_async_copy_from_s3_to_s3(source, destination))

from typing import Callable
from threading import Thread

def _run_aysnc(func_async: Callable, *args) -> None:
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(func_async(*args))


def _run_threaded_async(func_async: Callable, *args):
    t = Thread(target=_run_aysnc, args=(func_async, *args))
    t.start()
    t.join()


async def _async_copy_from_s3_to_s3(
    source: _CopySource, destination: _CopyDestination
) -> None:
    session = aiobotocore.get_session()
    config = AioConfig(max_pool_connections=MAX_POOL_CONNECTIONS)
    copy_operations = []
    counter = 0
    async with session.create_client(
        "s3", region_name="eu-central-1", config=config
    ) as client:
        async for source_object in _list_objects_to_copy(client, source):
            destination_object = _destination_object_for(destination, counter)
            counter += 1
            # use create_task to start the copy without waiting for the _list_objects_to_copy call
            copy_task = asyncio.create_task(
                _copy_object(client, source_object, destination_object)
            )
            copy_operations.append(copy_task)
        await asyncio.gather(*copy_operations)


def _destination_object_for(destination: _CopyDestination, counter: int) -> _CopyDestinationObject:
    return _CopyDestinationObject(
        bucket=destination.bucket,
        key="".join([destination.key_prefix, ".", str(counter), ".parquet"]),
    )


async def _list_objects_to_copy(
    client, source: _CopySource
) -> AsyncIterator[_CopySourceObject]:
    paginator = client.get_paginator("list_objects_v2")
    async for result in paginator.paginate(
        Bucket=source.bucket, Prefix=source.key_prefix
    ):
        for item in result.get("Contents", []):
            yield _CopySourceObject(
                bucket=source.bucket, key=item["Key"], size_bytes=item["Size"]
            )


async def _copy_object(
    client, source: _CopySourceObject, dest: _CopyDestinationObject
) -> None:
    if source.size_bytes >= MULTIPART_COPY_OBJ_SIZE_THRESHOLD_BYTES:
        await _copy_object_multipart(client, source, dest)
        return
    await _copy_object_single_call(client, source, dest)


async def _upload_part_copy(
    *,
    client,
    source: _CopySourceObject,
    dest: _CopyDestinationObject,
    upload_id: int,
    part_number: int,
    range_start: int,
    range_end: int,
) -> _UploadPartCopyResult:
    res = await client.upload_part_copy(
        Bucket=dest.bucket,
        Key=dest.key,
        UploadId=upload_id,
        PartNumber=part_number,
        CopySource={"Bucket": source.bucket, "Key": source.key},
        CopySourceRange=f"bytes={range_start}-{range_end}",
    )
    return _UploadPartCopyResult(
        etag=res["CopyPartResult"]["ETag"], part_number=part_number
    )


async def _copy_object_multipart(
    client, source: _CopySourceObject, dest: _CopyDestinationObject
) -> None:
    res = await client.create_multipart_upload(
        Bucket=dest.bucket, Key=dest.key, ACL="bucket-owner-full-control"
    )
    upload_id = res["UploadId"]
    copy_operations = []
    range_start = 0
    part_number = 1
    while range_start < source.size_bytes:
        range_end = min(range_start + MULTIPART_COPY_PART_SIZE, source.size_bytes) - 1
        copy_operations.append(
            _upload_part_copy(
                client=client,
                source=source,
                dest=dest,
                upload_id=upload_id,
                part_number=part_number,
                range_start=range_start,
                range_end=range_end,
            )
        )
        range_start += MULTIPART_COPY_PART_SIZE
        part_number += 1
    results = await asyncio.gather(*copy_operations)
    # No error handling here - server-side, we have a bucket policy to delete incomplete multipart uploads.
    await client.complete_multipart_upload(
        Bucket=dest.bucket,
        Key=dest.key,
        UploadId=upload_id,
        MultipartUpload={
            "Parts": [
                {"ETag": result.etag, "PartNumber": result.part_number}
                for result in results
            ],
        },
    )


async def _copy_object_single_call(
    client, source: _CopySourceObject, dest: _CopyDestinationObject
) -> None:
    await client.copy_object(
        Bucket=dest.bucket,
        Key=dest.key,
        CopySource={"Bucket": source.bucket, "Key": source.key},
        ACL="bucket-owner-full-control",
    )
    return
