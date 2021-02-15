import os, time, datetime

def get_present_year() -> int:
    return datetime.datetime.today().year

def get_present_month() -> int:
    return datetime.datetime.today().month

def get_present_day() -> int:
    return datetime.datetime.today().day

def get_present_hour() -> int:
    return datetime.datetime.today().hour

def get_present_minute() -> int:
    return datetime.datetime.today().minute

def get_present_second() -> int:
    return datetime.datetime.today().second

def get_present_microsecond() -> int:
    return datetime.datetime.today().microsecond

def get_present_time() -> str:
    return datetime.datetime.today().strftime('%Y/%m/%d %H:%M:%S')

def get_present_time_Ymd() -> str:
    return datetime.datetime.today().strftime('%Y/%m/%d')

def get_present_time_HMS() -> str:
    return datetime.datetime.today().strftime('%H:%M:%S')

def get_ctime(path: str) -> str:
    return time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime(os.path.getctime(path)))

def get_ctime_Ymd(path: str) -> str:
    return time.strftime("%Y/%m/%d", time.gmtime(os.path.getctime(path)))

def get_ctime_HMS(path: str) -> str:
    return time.strftime("%H:%M:%S", time.gmtime(os.path.getctime(path)))

def get_mtime(path: str) -> str:
    return time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime(os.path.getmtime(path)))

def get_mtime_Ymd(path: str) -> str:
    return time.strftime("%Y/%m/%d", time.gmtime(os.path.getmtime(path)))

def get_mtime_HMS(path: str) -> str:
    return time.strftime("%H:%M:%S", time.gmtime(os.path.getmtime(path)))

def duration_to_HMS(duration: int) -> str:
    return time.strftime("%H:%M:%S", time.gmtime(duration))

# Time usec based functions
def get_utc_time_from_time_usec(time_usec: int) -> datetime.datetime:
    return datetime.datetime.utcfromtimestamp(time_usec/(10**6))

def get_utc_time_elapsed_from_time_usec(time_usec: int) -> datetime.timedelta:
    return datetime.datetime.now() - get_utc_time_from_time_usec(time_usec)

def get_days_elapsed_from_time_usec(time_usec: int) -> float:
    time_elapsed = get_utc_time_elapsed_from_time_usec(time_usec)
    return time_elapsed.days + (time_elapsed.seconds / (24*3600)) + (time_elapsed.microseconds / (24*3600*10**6))

def get_years_elapsed_from_time_usec(time_usec: int) -> float:
    return get_days_elapsed_from_time_usec(time_usec) / 365