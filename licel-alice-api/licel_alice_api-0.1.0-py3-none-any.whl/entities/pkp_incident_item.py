from typing import List

from .incident_item import IncidentItem
from ..utils import DictWrapper, dict_prop


class PKPContentData(DictWrapper):
    date_time: str = dict_prop()
    effective_expiration_date: int = dict_prop()
    hostname: str = dict_prop()
    include_subdomains: bool = dict_prop()
    known_pins: List[str] = dict_prop()
    noted_hostname: str = dict_prop()
    port: int = dict_prop()
    served_certificate_chain: List[str] = dict_prop()
    validated_certificate_chain: List[str] = dict_prop()


class PKPIncidentItemContent(DictWrapper):
    pkp: PKPContentData = dict_prop(wrapper=PKPContentData)


class PKPIncidentItem(IncidentItem):
    content: PKPIncidentItemContent = dict_prop(wrapper=PKPIncidentItemContent)
