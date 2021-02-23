import threading
from thread_signals.task_broker import Task_broker


def get_func_patcher(executor_thread_id, timeout, sync_call = True):
    def func_patcher(orig_func):
        return simple_func_patcher(orig_func, executor_thread_id, timeout, sync_call)

    return func_patcher


def simple_func_patcher(orig_func, executor_thread_id, timeout, sync_call = True):
    def patched_func(*args, **kwargs):
        if threading.get_ident() == executor_thread_id:
            return orig_func(*args, **kwargs)

        # print("Task added for call " + orig_func.__name__ + "(" + ", ".join(
        #     [str(i) for i in args] + [str(name) + "=" + str(value) for (name, value) in kwargs.items()]) + ")")

        broker = Task_broker.get_task_broker(executor_thread_id)
        res = broker.run_func_as_task(orig_func, args, kwargs, timeout, sync_call)

        #nothing to wait
        if not sync_call:
            return

        #analyze response if sync call
        if type(res) is bool:
            raise Exception("Command {fnc_name} not run in {timeout} seconds".format(fnc_name=orig_func.__name__,
                                                                                     timeout=str(timeout)))

        if res[0] is False:
            raise res[2]
        else:
            return res[1]


    return patched_func


def interface_patcher(interface_class, executor_thread, timeout):
    #get name
    if not isinstance(interface_class, type):
        raise Exception("Interface must be type object!")

    new_name = interface_class.__name__

    #make attrs
    patcher = get_func_patcher(executor_thread, timeout)
    attrs = {}
    for att_name in vars(interface_class):
        if att_name.startswith("_"):
            continue

        attr_val = getattr(interface_class, att_name)
        if not callable(attr_val):
            continue

        attrs[att_name] = patcher(attr_val)

    new_class = type(new_name, (object,), attrs)
    return new_class