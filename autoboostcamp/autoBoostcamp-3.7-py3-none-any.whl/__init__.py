__all__ = ["backend"]

from .backend import doHi, doBye, quick_start
import datetime

def do():
    now = datetime.datetime.now()
    if now.weekday() in [5,6]: # 토요일, 일요일
        return

    now_hm = now.hour + 0.01 * now.minute
    if 9.30 <= now_hm <= 10.05:  # 9시 30분 ~ 10시5분
        print(f"autoBoostcamp doHi run")
        doHi()

    elif now_hm >= 19:  # 19시 ~
        print(f"autoBoostcamp doBye run")
        doBye()