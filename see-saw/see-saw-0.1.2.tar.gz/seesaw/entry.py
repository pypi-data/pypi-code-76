import argparse
import json
import os
import random
import sys
from datetime import datetime, timedelta, timezone
from threading import Thread
from typing import Callable, Tuple

import boto3
import sqlalchemy
import urwid
from dateutil import tz
from sqlalchemy.sql import or_

from seesaw import storage
from seesaw.log_factory import polling_worker_entry
from seesaw.config import LOG_DIR, SETTINGS, USER_DIR, logger

log = logger(__file__)
localtz = tz.tzlocal()


def random_hex():
    return "".join(random.choice("abcdef1234567890") for _ in range(10))


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--show-log-file",
        action="store_true",
        help="display the path to this app's log file",
    )
    args = parser.parse_args()
    log.info("launched", args=vars(args))

    if args.show_log_file:
        print(str(LOG_DIR / "logs.json"))
        return

    try:
        loop()
    except KeyboardInterrupt:
        sys.exit(3)


def d_widget(sawmill):
    def show_or_exit(key):
        if key in ("q", "Q"):
            raise urwid.ExitMainLoop()
        elif key in ("v", "V"):
            sawmill.toggle_date()
            sawmill.refresh_logs()
        elif key in ("r", "R"):
            sawmill.refresh_logs()

    return show_or_exit


class LogPollingManager:
    def __init__(self, session: sqlalchemy.orm.Session) -> None:
        self.pollers = {}
        self.session = session

    def pop_group(self, region, log_group_name):
        try:
            self.active.remove((region, log_group_name))
        except KeyError:
            pass

    def push_group(self, region, log_group_name):
        # spin down all queries except ones for the current region
        storage.LiveReader.destroy_other_region_readers(self.session, region)

        thread_id = (region, log_group_name)
        if (
            storage.LiveReader.exists_for(self.session, region, log_group_name)
            and self.pollers.get(thread_id)
            and self.pollers[thread_id].is_alive()
        ):
            log.info("Thread was already alive", args=thread_id)
            return

        log.info(
            "Pushing new poller for log group",
            new=thread_id,
        )
        new_thread = storage.LiveReader(
            pid=os.getpid(), region=region, log_group=log_group_name
        )
        self.session.add(new_thread)
        self.session.commit()
        self.pollers[thread_id] = Thread(
            daemon=True,
            target=polling_worker_entry,
            args=(region, log_group_name),
        )
        self.pollers[thread_id].start()


class LogReadingPane:
    def __init__(self) -> None:
        self.messages = urwid.SimpleFocusListWalker([])
        self.viewer = urwid.ListBox(self.messages)
        self.db = storage.connect()
        self.poll_manager = LogPollingManager(self.db)
        self.verbose_dates = False

        for old_evt in (
            self.db.query(storage.Event)
            .filter(
                storage.Event.timestamp
                < (datetime.now(tz=timezone.utc) - timedelta(hours=8)).isoformat()
            )
            .all()
        ):
            log.info("Deleting", e=old_evt.timestamp)
            self.db.delete(old_evt)
        self.db.commit()

        self.region_menu = TargetSelect()
        self.top = urwid.Columns([(90, self.region_menu), self.viewer], dividechars=2)

    def refresh_logs(self):
        region, groups = self.region_menu.get_selected_groups()
        for g in groups:
            self.poll_manager.push_group(region, g)
        try:
            log.info("querying local storage", region=region, groups=groups)
            self.messages.clear()
            for event in sorted(
                self.db.query(storage.Event)
                .filter(storage.Event.region == region)
                .filter(
                    storage.Event.timestamp
                    > (datetime.now(tz=timezone.utc) - timedelta(hours=8)).isoformat()
                )
                .filter(
                    or_(storage.Event.log_group == g for g in groups)
                )  # expands to the equivalent of `if Event.log_group in groups`
                .order_by(storage.Event.timestamp.desc())
                .limit(500)
                .all(),
                key=lambda e: datetime.fromisoformat(e.timestamp),
            ):
                log.debug("Found event", msg=event.message, gid=event.gid)
                self.new_message(event)
        except:
            log.exception("Error rendering log messages")

    def new_message(self, event):
        self.messages.append(urwid.Text(self.format_event(event)))
        self.viewer.focus_position = len(self.messages) - 1

    def toggle_date(self):
        self.verbose_dates = not self.verbose_dates

    def timestamp(self, ts):
        if self.verbose_dates:
            return (
                "timestamp",
                datetime.fromisoformat(ts)
                .astimezone(localtz)
                .strftime("%Y-%m-%d %H:%M:%S"),
            )
        return (
            "timestamp",
            datetime.fromisoformat(ts).astimezone(localtz).strftime("%H:%M:%S"),
        )

    def format_event(self, event):
        try:
            return [
                self.timestamp(event.timestamp),
                " ",
                json.dumps(json.loads(event.message), indent=2, sort_keys=True),
            ]
        except:
            return [
                self.timestamp(event.timestamp),
                " ",
                event.message,
            ]


class TargetSelect(urwid.WidgetWrap):
    def __init__(self):
        self.regions = [r[0] for r in initial_options()]
        self.options = []

        group_select = GroupSelect(get_selected_region=self.get_state)
        self._selected_groups = group_select.get_state

        def update_region_selection(caller_widget, new_state):
            if not new_state:
                log.info("User region deselected", region=caller_widget._label._text)
                return
            log.info("User region selected", region=caller_widget._label._text)
            group_select.change_region(caller_widget._label._text)

        widgets = [
            urwid.RadioButton(
                self.options,
                region_name,
                state=(region_name == SETTINGS["presets"]["default"]["region"]),
                on_state_change=update_region_selection,
            )
            for region_name in self.regions
        ]
        region_list = urwid.ListBox(widgets)
        display_widget = urwid.Columns(
            [(18, region_list), (70, group_select)], dividechars=2
        )
        urwid.WidgetWrap.__init__(self, display_widget)

    def get_selected_groups(self) -> Tuple[str, set]:
        return self.get_state(), self._selected_groups()

    def get_state(self):
        for o in self.options:
            if o.get_state() is True:
                return o.get_label()


def abbreviate_group_name(name: str) -> str:
    if name.startswith("/aws/lambda/"):
        return name.replace("/aws/lambda/", "λ ")
    if name.startswith("/aws/vendedlogs/states/"):
        return name.replace("/aws/vendedlogs/states/", "SF ")
    if name.startswith("API-Gateway-Execution-Logs_"):
        return name.replace("API-Gateway-Execution-Logs_", "API-Exec-")
    return name


def unmask_group_name(name: str) -> str:
    if name.startswith("λ "):
        return name.replace("λ ", "/aws/lambda/")
    if name.startswith("SF "):
        return name.replace("SF ", "/aws/vendedlogs/states/")
    if name.startswith("API-Exec-"):
        return name.replace("API-Exec-", "API-Gateway-Execution-Logs_")
    return name


class GroupSelect(urwid.WidgetWrap):
    def __init__(self, get_selected_region: Callable):
        self.client_map = dict(initial_options())
        self.selected_groups = set()
        self.current_region = (
            get_selected_region() or SETTINGS["presets"]["default"]["region"]
        )
        self.get_selected_region = get_selected_region
        urwid.WidgetWrap.__init__(
            self, self.build_group_checkboxes(self.current_region)
        )

    def toggle_group_select(self, widget, active: bool):
        log.info(
            "log group selected",
            value=active,
            group_name=unmask_group_name(widget.get_label()),
        )
        if active:
            self.selected_groups.add(unmask_group_name(widget.get_label()))
        else:
            self.selected_groups.remove(unmask_group_name(widget.get_label()))

    def get_state(self):
        return list(self.selected_groups)

    def change_region(self, region_name):
        if region_name == self.current_region:
            return
        # clear out group selections since we are swapping region
        self.selected_groups = set()
        self.current_region = region_name
        log.info("loading region groups", region=region_name)
        self._w = self.build_group_checkboxes(region_name)
        log.info("region swap done", region=region_name)

    def build_group_checkboxes(self, region_name: str):
        return urwid.ListBox(
            [
                urwid.CheckBox(
                    abbreviate_group_name(g["name"]),
                    on_state_change=self.toggle_group_select,
                )
                for g in self.client_map[region_name]()
            ]
        )


def loop():
    reader = LogReadingPane()
    loop = urwid.MainLoop(
        reader.top,
        {
            ("timestamp", "dark red", "light gray"),
        },
        unhandled_input=d_widget(reader),
    )
    loop.run()


def initial_options():
    if (USER_DIR / "regions.json").exists():
        with open(USER_DIR / "regions.json") as rjson:
            regions = json.load(rjson)
    else:
        regions = boto3.Session().get_available_regions("logs")
        with open(USER_DIR / "regions.json", "w") as rjson:
            json.dump(regions, rjson)
    for r in regions:
        yield (r, groups_in_region(r))


def groups_in_region(region_name):
    s = boto3.Session(region_name=region_name)
    logs = s.client("logs")

    def regional_logs():
        """Keeps `region_name` inside a closure that will list log groups in that region"""
        try:
            pager = (
                logs.get_paginator("describe_log_groups")
                .paginate()
                .search(
                    "logGroups[].{name: logGroupName, size: storedBytes, created: creationTime}"
                )
            )
            for group in pager:
                since_created = datetime.now(tz=timezone.utc) - datetime.fromtimestamp(
                    group["created"] / 1000, tz=timezone.utc
                )

                if group["size"] or since_created < timedelta(hours=8):
                    group["region"] = region_name
                    yield group
        except logs.exceptions.UnrecognizedClientException:
            pass

    return regional_logs
