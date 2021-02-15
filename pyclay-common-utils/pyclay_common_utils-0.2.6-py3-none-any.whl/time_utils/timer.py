import time
from logger import logger
from ..check_utils import check_key_not_in_dict, check_key_in_dict
from .time_utils import duration_to_HMS

class TimerStates:
    RESET = 0
    STARTED = 1
    STOPPED = 2

    @classmethod
    def to_str(self, state: int) -> str:
        if state == self.RESET:
            return 'RESET'
        elif state == self.STARTED:
            return 'STARTED'
        elif state == self.STOPPED:
            return 'STOPPED'
        else:
            logger.error(f"Invalid state index: {state}")
            raise Exception

    @classmethod
    def check_state(self, input_state: int, valid_states: list):
        if input_state not in valid_states:
            logger.error(f"Invalid state: {self.to_str(input_state)}")
            expected_str = ""
            if len(valid_states) == 0:
                logger.error(f"valid_states have not been provided")
                raise Exception
            for i, valid_state in zip(range(len(valid_states)), valid_states):
                if i == 0:
                    expected_str += f"{self.to_str(valid_state)}"
                else:
                    expected_str += f", {self.to_str(valid_state)}"
            logger.error(f"Expected: {expected_str}")
            raise Exception

class TimerHandler:
    def __init__(self):
        self.timers = {}

    def tick(self, label: str):
        check_key_not_in_dict(item_dict=self.timers, key=label)
        self.stop_and_print()
        self.start(label)

    def last_tick(self):
        self.stop_and_print()

    def start(self, label: str):
        if label not in self.timers:
            self.add_timer(label)
        else:
            self.reset_timer(label, key_check=False)
        self.start_timer(label, key_check=False)

    def stop(self, label: str):
        self.stop_timer(label, key_check=True)

    def stop_and_print(self):
        for key in self.timers:
            timer = self.timers[key]
            state = timer['state']
            if state == TimerStates.STARTED:
                self.stop_timer(key, key_check=False)
                logger.info(f"{key}: {self.get_time(key, key_check=False)}")

    def reset(self, label: str):
        self.reset_timer(label, key_check=True)

    def add_timer(self, key: str):
        check_key_not_in_dict(item_dict=self.timers, key=key)
        self.timers[key] = {'start': None, 'end': None, 'state': TimerStates.RESET}

    def reset_timer(self, key: str, key_check: bool=True):
        if key_check:
            check_key_in_dict(item_dict=self.timers, key=key)
        timer = self.timers[key]
        state = timer['state']
        TimerStates.check_state(input_state=state, valid_states=[TimerStates.STARTED, TimerStates.STOPPED])
        self.timers[key] = {'start': None, 'end': None, 'state': TimerStates.RESET}

    def start_timer(self, key: str, key_check: bool=True):
        if key_check:
            check_key_in_dict(item_dict=self.timers, key=key)
        timer = self.timers[key]
        state = timer['state']
        TimerStates.check_state(input_state=state, valid_states=[TimerStates.RESET])
        timer = {'start': time.time(), 'end': None, 'state': TimerStates.STARTED}
        self.timers[key] = timer

    def stop_timer(self, key: str, key_check: bool=True):
        if key_check:
            check_key_in_dict(item_dict=self.timers, key=key)
        timer = self.timers[key]
        state = timer['state']
        TimerStates.check_state(input_state=state, valid_states=[TimerStates.STARTED])
        start = timer['start']
        if start is None:
            logger.error(f"Tried to stop timer {key}, but start time is None.")
            raise Exception
        timer = {'start': start, 'end': time.time(), 'state': TimerStates.STOPPED}
        self.timers[key] = timer

    def get_time(self, key: str, key_check: bool=True) -> str:
        if key_check:
            check_key_in_dict(item_dict=self.timers, key=key)
        timer = self.timers[key]
        state = timer['state']
        TimerStates.check_state(input_state=state, valid_states=[TimerStates.STOPPED])
        start, end = timer['start'], timer['end']
        if start is None:
            logger.error(f"Tried to get duration from timer {key}, but start time is None.")
            raise Exception
        if end is None:
            logger.error(f"Tried to get duration from timer {key}, but end time is None.")
            raise Exception
        duration = end - start
        return duration_to_HMS(duration)

    def reset_all(self):
        for key in self.timers:
            self.reset_timer(key=key, key_check=False)

    def add_timers(self, key_list: list):
        for key in key_list:
            self.add_timer(key)

    def timer_summary(self):
        for key in self.timers:
            timer = self.timers[key]
            state = timer['state']
            if state == TimerStates.RESET:
                logger.blue(f"{key}: RESET")
            elif state == TimerStates.STARTED:
                logger.red(f"{key}: STARTED")
            elif state == TimerStates.STOPPED:
                logger.green(f"{key}: {self.get_time(key, key_check=False)}")