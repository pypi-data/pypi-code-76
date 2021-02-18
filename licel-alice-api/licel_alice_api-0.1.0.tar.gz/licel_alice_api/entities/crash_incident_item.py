from typing import List

from .incident_item import IncidentItem
from ..utils import DictWrapper, dict_prop, DictListWrapper


class CrashContentThread(DictWrapper):
    crashed: str = dict_prop()
    requesting_thread: int = dict_prop()
    frames_map: List[str] = dict_prop()
    cause: List[str] = dict_prop()
    frames: List[str] = dict_prop()


class CrashContentData(DictWrapper):
    crash_address: str = dict_prop()
    reason: str = dict_prop()
    threads: DictListWrapper[CrashContentThread] = dict_prop(
        is_list=True, wrapper=CrashContentThread
    )
    type: str = dict_prop()
    uptime_sec: int = dict_prop()


class CrashIncidentItemContent(DictWrapper):
    crash: CrashContentData = dict_prop(wrapper=CrashContentData)


class CrashIncidentItem(IncidentItem):
    content: CrashIncidentItemContent = dict_prop(wrapper=CrashIncidentItemContent)
