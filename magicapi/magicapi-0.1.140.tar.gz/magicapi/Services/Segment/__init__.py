import analytics

from magicapi import g

from magicapi.Decorators.background_tasks import run_in_background

analytics.write_key = g.settings.segment_write_key
analytics.sync_mode = True


@run_in_background
def identify(*args, **kwargs):
    return analytics.identify(*args, **kwargs)


@run_in_background
def track(*args, **kwargs):
    return analytics.track(*args, **kwargs)


@run_in_background
def page(*args, **kwargs):
    return analytics.page(*args, **kwargs)


@run_in_background
def screen(*args, **kwargs):
    return analytics.screen(*args, **kwargs)


@run_in_background
def group(*args, **kwargs):
    return analytics.group(*args, **kwargs)


@run_in_background
def alias(*args, **kwargs):
    return analytics.alias(*args, **kwargs)
