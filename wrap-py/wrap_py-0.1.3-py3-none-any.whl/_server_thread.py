import threading, time


from wrap_py import wrap_base

from thread_signals import LateStartThread, get_thread_broker, interface_patcher, get_func_patcher


#run in App thread
def on_every_app_tick():
    broker = get_thread_broker()
    broker.run_all_tasks()

#starter of App thread
def app_starter():
    wrap_base.app.start(on_tick=on_every_app_tick)

#starter of Callback thread
def callback_starter():
    broker = get_thread_broker()
    while True:
        broker.run_all_tasks(True)
        time.sleep(1/100)


def start_app_thread(interfaces_list, call_timeout=None):
    #make thread
    app_thread = LateStartThread(target=app_starter, name="App thread")

    #patch interaces
    res = []
    for i in interfaces_list:
        new = interface_patcher(i, app_thread.ident, call_timeout)
        res.append(new)

    #start callback thread
    cb_thread = threading.Thread(target=callback_starter, name="Callback thread", daemon=True)
    cb_thread.start()

    #make callback patcher
    callback_patcher = get_func_patcher(cb_thread.ident, call_timeout, False)

    # start app work
    app_thread.start()

    return {
        "patched_interfaces": res,
        "callback_func_patcher" : callback_patcher
    }


def event_handler_hook(orig_func):
    return orig_func

