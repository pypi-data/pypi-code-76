from typing import List
import os
import time
from datetime import datetime, timedelta, timezone

import boto3

from seesaw import storage
from seesaw.config import logger

log = logger(__file__)


class PolitePoller:
    def __init__(
        self, region: str, logs_client: boto3.client, start_time: datetime = None
    ):
        self.region = region
        self.start_time = start_time or datetime.now(tz=timezone.utc)
        self.logs = logs_client or boto3.client("logs")

    def poller_with_breaks(self, group_name: str, start_time: datetime = None):
        kwargs = {
            "logGroupName": group_name,
            "interleaved": True,
        }
        if start_time is None:
            kwargs["startTime"] = int(self.start_time.timestamp()) * 1000
        else:
            kwargs["startTime"] = int(start_time.timestamp()) * 1000
        while True:
            paginator = self.logs.get_paginator("filter_log_events").paginate(**kwargs)
            log.info("querying", kwargs=kwargs)
            for event in paginator.search("events[]"):
                # update the start time to when we start paginating through
                kwargs["startTime"] = int(
                    max(event["timestamp"] / 1000, kwargs["startTime"])
                )
                event["logGroupName"] = group_name
                event["region"] = self.region
                yield storage.Event.from_json(event)
            yield None


def polling_worker_entry(region, log_group_name):
    session = storage.connect()
    log.info("finding newest message we have")
    newest_msg: List[storage.Event] = (
        session.query(storage.Event)
        .filter(storage.Event.log_group == log_group_name)
        .filter(storage.Event.region == region)
        .order_by(storage.Event.timestamp.desc())
        .limit(1)
        .all()
    )
    if newest_msg:
        start_at = datetime.fromisoformat(newest_msg[0].timestamp)
        log.info(
            "found existing message",
            message_id=newest_msg[0].gid,
            start_at=start_at.isoformat(),
            event_time=newest_msg[0].timestamp,
        )
    else:
        start_at = datetime.now(tz=timezone.utc) - timedelta(hours=4)
    pp = PolitePoller(
        region=region,
        logs_client=boto3.client("logs", region_name=region),
        start_time=start_at,
    )
    session.add(
        storage.LiveReader(
            pid=os.getpid(),
            log_group=log_group_name,
            region=region,
        )
    )
    session.commit()
    log.info("Instantiated poller", region=region, group=log_group_name)
    for msg in pp.poller_with_breaks(group_name=log_group_name):
        if msg is None:
            try:
                session.commit()
                log.info("Saved writes to DB")
            except:
                log.exception("Error committing writes to DB")
            # betweeen message groups, sleep for 10 seconds
            log.info("awaiting more logs", region=region, log_group_name=log_group_name)
            # TODO(rsb): check if we are still supposed to be running
            if storage.LiveReader.exists_for(session, region, log_group_name):
                time.sleep(10)
            else:
                log.info(
                    "self not found in active threads",
                    region=region,
                    log_group_name=log_group_name,
                )
                break
        else:
            try:
                if (
                    session.query(storage.Event)
                    .filter(storage.Event.gid == msg.gid)
                    .one_or_none()
                    is None
                ):
                    session.add(msg)
                    log.info("Added log from", group=msg.log_group, ts=msg.timestamp)
                    session.commit()
            except:
                log.exception("could not add message to DB")