import time

def retry(waiting_time, limit, proc, args):
    result = None
    for _ in range(limit):
        try:
            result = proc(args)
        except:
            time.sleep(waiting_time)
        else:
            break

    return result
