# Copyright 2020-2021 Cambridge Quantum Computing
#
# You may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html

"""Status classes for circuits submitted to backends.
"""
from typing import NamedTuple
from enum import Enum


class StatusEnum(Enum):
    """Enumeration for the possible status of a circuit submitted to a backend."""

    COMPLETED = "Circuit has completed. Results are ready."
    QUEUED = "Circuit is queued."
    SUBMITTED = "Circuit has been submitted."
    RUNNING = "Circuit is running."
    CANCELLED = "Circuit has been cancelled."
    ERROR = "Circuit has errored. Check CircuitStatus.message for error message."


class CircuitStatus(NamedTuple):
    """The status of a circuit along with optional long description, \
for example an error message."""

    status: StatusEnum
    message: str = ""


WAITING_STATUS = {StatusEnum.QUEUED, StatusEnum.SUBMITTED, StatusEnum.RUNNING}
