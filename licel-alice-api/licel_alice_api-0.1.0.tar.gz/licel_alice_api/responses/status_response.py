from enum import Enum

from ..utils import DictWrapper, dict_prop


class Status(Enum):
    OK = "OK"
    FAIL = "FAIL"
    BAD_EXPRESSION = "BAD_EXPRESSION"

    def __str__(self):
        return str(self.value)


class StatusData(DictWrapper):
    status: Status = dict_prop(wrapper=Status)
    desc: str = dict_prop()


class StatusResponse(DictWrapper):
    status: StatusData = dict_prop(wrapper=StatusData)
