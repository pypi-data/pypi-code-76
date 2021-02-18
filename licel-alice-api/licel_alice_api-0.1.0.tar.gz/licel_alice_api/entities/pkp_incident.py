from .incident import Incident
from ..utils import dict_prop


class PKPIncident(Incident):
    hostname: str = dict_prop()
    hostname_port: str = dict_prop()
    port: int = dict_prop()
