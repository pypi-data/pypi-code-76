from datetime import datetime


def get_date_and_time():
    now = datetime.now()
    now_date = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
    now_time = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
    return now_date, now_time
