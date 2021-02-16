from datetime import datetime, timedelta

BUFFER_DURATION_IN_MINUTES = 10


def get_buffered_timestamp(timestamp: str):
    """
    Adds ten minutes buffer to given start date

    :param timestamp: start date
    :return: buffered start date
    """
    start = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") - timedelta(
        minutes=BUFFER_DURATION_IN_MINUTES
    )
    return start.strftime("%Y-%m-%d %H:%M:%S")
