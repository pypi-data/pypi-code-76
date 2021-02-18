from ..utils import DictWrapper, dict_prop


class MongoID(DictWrapper):
    counter: int = dict_prop()
    date: str = dict_prop()
    time: int = dict_prop()
    time_second: int = dict_prop()
    timestamp: int = dict_prop()
    machine_identifier: int = dict_prop()
    process_identifier: int = dict_prop()
