# Copyright 2020 Software Factory Labs, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional, Callable, Dict, Tuple, List
from datetime import datetime
import inspect
from .triggers import Trigger
from . import util


class Job:
    """
    A job to be executed by the executor.
    """
    def __init__(self,
                 func: Callable,
                 identifier: str,
                 args: Tuple,
                 kwargs: Dict,
                 dynamic_args: Dict[str, Callable],
                 trigger: Trigger,
                 next_run_time: Optional[datetime] = None,
                 description: Optional[str] = None,
                 coalesce: bool = False,
                 max_instances: int = -1,
                 active: bool = True,
                 callback: Optional[Callable] = None,
                 error_callback: Optional[Callable] = None):
        """
        Initialize the job.
        :param func: the function to be called when the job executes
        :param identifier: the unique ID of the job
        :param args: the arguments to pass to func
        :param kwargs: the keyword arguments to pass to func
        :param dynamic_args: a dictionary of argument names mapping to functions that will be executed upon job
            execution. the return values of the functions will be passed to func as keyword arguments
        :param trigger: the trigger to used to determine when the job will execute
        :param next_run_time: the next run time of the job. if None, the next run time will be determined by the trigger
        :param description: the description of the job
        :param coalesce: if True, will only run once when several run times are due
        :param max_instances: the maximum number of concurrently running instances of the job. -1 means no limit, 0
            means disabled
        :param callback: a function to call if func executes successfully. it must accept three arguments: job_id,
            instance_id, and retval. the retval argument will be the return value of func
        :param error_callback: a function to call if func raises an exception. it must accept three arguments: job_id,
            instance_id, and exc. the exc argument will be the exception instance
        """
        self.func = func
        self.id = identifier
        self.args = args
        self.kwargs = kwargs
        self.trigger = trigger
        self.next_run_time = next_run_time
        self.description = description
        self.coalesce = coalesce
        self.max_instances = max_instances
        self.active = active

        try:
            self.func_ref = util.obj_to_ref(self.func)
        except ValueError:
            self.func_ref = None

        if callback is None:
            self.callback = dummy_callback
        else:
            self.callback = callback

        if error_callback is None:
            self.error_callback = dummy_callback
        else:
            self.error_callback = error_callback

        try:
            self.callback_ref = util.obj_to_ref(self.callback)
        except ValueError:
            self.callback_ref = None

        try:
            self.error_callback_ref = util.obj_to_ref(self.error_callback)
        except ValueError:
            self.error_callback_ref = None

        self.dynamic_args = {}
        for arg_name, arg_func in dynamic_args.items():
            try:
                arg_func_ref = util.obj_to_ref(arg_func)
            except ValueError:
                arg_func_ref = None

            self.dynamic_args[arg_name] = {'func': arg_func, 'func_ref': arg_func_ref}

    def _modify(self, **changes):
        pass

    def _get_run_times(self, latest: datetime) -> List[datetime]:
        run_times = []
        next_run_time = self.next_run_time
        while next_run_time and next_run_time < latest:
            run_times.append(next_run_time)
            next_run_time = self.trigger.get_next_fire_time(next_run_time, latest)
        return run_times

    def get_next_run_time_ts(self):
        return self.next_run_time.timestamp() if self.next_run_time is not None else None

    def __getstate__(self):
        if self.func_ref is None:
            raise Exception(f'Job function ({self.func}) not serializable')

        if self.callback_ref is None:
            raise Exception(f'Job callback function ({self.callback}) not serializable')

        if self.error_callback_ref is None:
            raise Exception(f'Job error callback function ({self.error_callback}) not serializable')

        dynamic_args = {}
        for arg_name, values in self.dynamic_args.items():
            func = values['func']
            func_ref = values['func_ref']
            if func_ref is None:
                raise Exception(f'Job dynamic arg function ({func}) not serializable')
            dynamic_args[arg_name] = func_ref

        if inspect.ismethod(self.func) and not inspect.isclass(self.func.__self__):
            args = (self.func.__self__,) + tuple(self.args)
        else:
            args = self.args

        return {
            'id': self.id,
            'func': self.func_ref,
            'args': args,
            'kwargs': self.kwargs,
            'dynamic_args': dynamic_args,
            'trigger': self.trigger,
            'next_run_time': self.next_run_time,
            'description': self.description,
            'coalesce': self.coalesce,
            'max_instances': self.max_instances,
            'active': self.active,
            'callback': self.callback_ref,
            'error_callback': self.error_callback_ref,
        }

    def __setstate__(self, state):
        self.id = state['id']

        self.func_ref = state['func']
        self.func = util.ref_to_obj(self.func_ref)

        self.args = state['args']
        self.kwargs = state['kwargs']
        self.trigger = state['trigger']
        self.next_run_time = state['next_run_time']
        self.description = state['description']
        self.coalesce = state['coalesce']
        self.max_instances = state['max_instances']
        self.active = state['active']

        self.callback_ref = state['callback']
        self.callback = util.ref_to_obj(self.callback_ref)

        self.error_callback_ref = state['error_callback']
        self.error_callback = util.ref_to_obj(self.error_callback_ref)

        self.dynamic_args = {}
        for arg_name, func_ref in state['dynamic_args'].items():
            self.dynamic_args[arg_name] = {'func': util.ref_to_obj(func_ref), 'func_ref': func_ref}

    def __eq__(self, other):
        if isinstance(other, Job):
            return self.id == other.id
        return NotImplemented

    def __repr__(self):
        return f'<Job (id={self.id})>'

    def __str__(self):
        status = f'next run at: {self.next_run_time}' if self.next_run_time is not None else 'INACTIVE'
        return f'{self.id} (trigger: {self.trigger}, {status})'


def dummy_callback(x, y, z):
    pass
