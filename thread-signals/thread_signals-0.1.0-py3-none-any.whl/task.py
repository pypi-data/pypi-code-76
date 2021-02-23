import sys, threading, json

from tblib import pickling_support
pickling_support.install()
import pickle

class Task(threading.Event):
    def __init__(self, executor_thread_id, not_serialized_data, serialized_data):
        threading.Event.__init__(self)

        self._executor_thread_id = executor_thread_id

        self._not_serialized_data = not_serialized_data
        self._serialized_data = json.dumps(serialized_data, indent=True)

        self._result_success = None
        self._result_data = None
        self._excdata = None

    def run_task(self):
        if self.is_set():
            raise Exception('Task could only be run once!')

        if self._executor_thread_id != threading.get_ident():
            raise Exception('Task could only be run from executor thread!')

        try:
            serialized_data = json.loads(self._serialized_data)
            res = self._do_task(self._not_serialized_data, serialized_data)

        except Exception as e:
            self._set_exception(e)
        else:
            self._set_result(res)

        self.set()

    def _do_task(self, not_serialized_data, serialized_data):
        raise Exception('Method must be overriden!')

    def _set_exception(self, e):
        self._result_success = False
        self._excdata = pickle.dumps(sys.exc_info())

    def _set_result(self, res):
        self._result_success = True
        self._result_data = json.dumps(res)

    def is_successful(self):
        if not self.is_set():
            raise Exception('Task not run yet!')

        return self._result_success

    def get_exception(self):
        if not self.is_set():
            raise Exception('Task not run yet!')

        if self._excdata is None:
            return None

        #re create exception object
        exc_data =  pickle.loads(self._excdata)
        exc_obj = exc_data[0](exc_data[1])
        exc_obj.with_traceback(exc_data[2])
        return exc_obj

    def get_result(self):
        if not self.is_set():
            raise Exception('Task not run yet!')

        if self._result_data is None:
            return None

        return json.loads(self._result_data)



class TaskFuncRun(Task):
    def _save_args(self, func, args, kwargs):
        args=[*args]
        kwargs={**kwargs}

        # save callable params without serializing
        new_args = []
        for i in range(0, len(args)):
            val = args[i]
            if not callable(val):
                new_args.append(None)
            else:
                new_args.append(val)
                args[i] = None

        new_kwargs = {}
        for (i, val) in kwargs.items():
            if not callable(val):
                new_kwargs[i] = None
            else:
                new_kwargs[i] = val
                kwargs[i] = None

        return [func, new_args, new_kwargs], [args, kwargs]

    def _load_args(self, not_serialized, serialized):
        func = not_serialized[0]

        callable_args = not_serialized[1]
        callable_kwargs = not_serialized[2]

        cleared_args = serialized[0]
        cleared_kwargs = serialized[1]

        for i in range(0, len(callable_args)):
            callable_val = callable_args[i]
            if callable_val is None:
                continue

            cleared_args[i] = callable_val

        for (i, callable_val) in callable_kwargs.items():
            if callable_val is None:
                continue
            cleared_kwargs[i] = callable_val

        return [func, cleared_args, cleared_kwargs]

    def __init__(self, executor_thread_id, func, args, kwargs):

        not_serialized, serialized = self._save_args(func, args, kwargs)

        Task.__init__(self, executor_thread_id, not_serialized, serialized)

    def _do_task(self, not_serialized_data, serialized_data):
        func, args, kwargs = self._load_args(not_serialized_data, serialized_data)
        return func(*args, **kwargs)

