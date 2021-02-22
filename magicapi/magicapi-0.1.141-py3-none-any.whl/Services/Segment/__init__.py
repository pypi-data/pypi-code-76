import analytics

from magicapi import g

from magicapi.Decorators.background_tasks import run_in_background

analytics.write_key = g.settings.segment_write_key
analytics.sync_mode = True

from datetime import datetime


def date_hook(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.fromisoformat(value)
        except Exception as e:
            pass
    return json_dict


@run_in_background(object_hook=date_hook)
def identify(*args, **kwargs):
    return analytics.identify(*args, **kwargs)


@run_in_background(object_hook=date_hook)
def track(*args, **kwargs):
    return analytics.track(*args, **kwargs)


@run_in_background(object_hook=date_hook)
def page(*args, **kwargs):
    return analytics.page(*args, **kwargs)


@run_in_background(object_hook=date_hook)
def screen(*args, **kwargs):
    return analytics.screen(*args, **kwargs)


@run_in_background(object_hook=date_hook)
def group(*args, **kwargs):
    return analytics.group(*args, **kwargs)


@run_in_background(object_hook=date_hook)
def alias(*args, **kwargs):
    return analytics.alias(*args, **kwargs)
