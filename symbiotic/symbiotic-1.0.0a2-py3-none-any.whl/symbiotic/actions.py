from datetime import datetime
from functools import partial
from typing import Callable, List, Union

from symbiotic.schedule import Schedule


class Action(object):

    def __init__(self, callback: Callable, *args, **kwargs):
        self._callback: partial = partial(callback, *args, **kwargs)
        self._schedule: Union[Schedule, None] = None
        self._next_execution: Union[datetime, None] = None

    def __repr__(self):
        rep = f'{self.__class__.__qualname__}:'
        rep += f' {self._callback.func.__name__},'
        rep += f' args: {self._callback.args},'
        rep += f' kwargs: {self._callback.keywords}'
        return rep

    def __call__(self):
        return self._callback()

    def set_schedule(self, schedule: Schedule) -> None:
        self._schedule = schedule
        self.schedule_next_execution()

    def should_execute(self):
        return datetime.now() > self._next_execution

    def schedule_next_execution(self):
        datetimes = [instant.next_datetime() for instant in self._schedule.instants()]
        self._next_execution = min(datetimes)  # get the earliest execution datetime


class ActionScheduler(object):

    def __init__(self):
        self.actions: List[Action] = []
        self._schedule: Union[Schedule, None] = None

    def start_session(self, schedule: Schedule):
        self._schedule = schedule

    def add(self, callback: Callable, *args, **kwargs):
        action = Action(callback, *args, *kwargs)
        action.set_schedule(self._schedule)
        self.actions.append(action)
        return action

    def end_session(self):
        self._schedule = None

    def run(self):
        for action in self.actions[:]:
            if action.should_execute():
                action()
                action.schedule_next_execution()
