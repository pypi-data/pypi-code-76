def get_path(datetime_object, metric_name):
    path: str = datetime_object.isoformat() + '/' + metric_name

    return path
