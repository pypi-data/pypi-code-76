from .incident_item import IncidentItem
from ..utils import DictWrapper, dict_prop


class TamperContentData(DictWrapper):
    apk_check: int = dict_prop()
    certificate_check: int = dict_prop()
    code_encryption_check: int = dict_prop()
    check_segments: int = dict_prop()


class TamperIncidentItemContent(DictWrapper):
    tamper_notification: TamperContentData = dict_prop(wrapper=TamperContentData)


class TamperIncidentItem(IncidentItem):
    content: TamperIncidentItemContent = dict_prop(wrapper=TamperIncidentItemContent)
