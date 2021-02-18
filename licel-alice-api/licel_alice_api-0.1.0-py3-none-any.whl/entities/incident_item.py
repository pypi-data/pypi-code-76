from .incident import IncidentType
from ..utils import DictWrapper, dict_prop


class IncidentItem(DictWrapper):
    id: int = dict_prop()
    type: IncidentType = dict_prop(wrapper=IncidentType)
    api_key: str = dict_prop()
    app_name: str = dict_prop()
    app_version: str = dict_prop()
    client_id: int = dict_prop()
    content: dict = dict_prop()
    country: str = dict_prop()
    fingerprint: str = dict_prop()
    remote_ip: str = dict_prop()
    seen: bool = dict_prop()
    time: str = dict_prop()
    uid: str = dict_prop()
    version: str = dict_prop()
