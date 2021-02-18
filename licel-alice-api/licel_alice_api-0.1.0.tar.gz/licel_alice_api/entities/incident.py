from enum import Enum

from .mongo_id import MongoID
from ..utils import DictWrapper, dict_prop


class IncidentType(Enum):
    PKP = "PKP"
    ENV_CHECK = "ENV_CHECK"
    TAMPER = "TAMPER_NOTIFICATION"
    CRASH = "CRASH"

    def __str__(self):
        return self.value


class IncidentShortType(Enum):
    PKP = "pkp"
    ENV_CHECK = "env_check"
    TAMPER = "tamper"
    CRASH = "crash"

    def __str__(self):
        return self.value


def incident_type_to_short(incident_type: IncidentType) -> IncidentShortType:
    return IncidentShortType[incident_type]


def incident_short_type_to_full(incident_type: IncidentShortType) -> IncidentType:
    return IncidentType[incident_type]


class Incident(DictWrapper):
    id: int = dict_prop()
    mongo_id: MongoID = dict_prop(name="_id", wrapper=MongoID)
    type: IncidentType = dict_prop(wrapper=IncidentType)
    api_key: str = dict_prop()
    app: str = dict_prop()
    app_version: str = dict_prop()
    client_id: int = dict_prop()
    country: str = dict_prop()
    fingerprint: str = dict_prop()
    os: str = dict_prop()
    os_and_version: str = dict_prop()
    os_version: str = dict_prop()
    project: str = dict_prop()
    project_id: int = dict_prop()
    remote_ip: str = dict_prop()
    seen: bool = dict_prop()
    time: int = dict_prop()
    uid: str = dict_prop()
    version: str = dict_prop()
