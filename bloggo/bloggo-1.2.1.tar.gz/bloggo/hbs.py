from datetime import datetime


def format_date(_, date_str, date_format):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    return date.strftime(date_format)
