
def get_time_difference(time1, time2, accurate=False):
    units = {1: ("millisecond", 0.01), 60: ("second", 1), 3600: ("minute", 60), 86400: ("hour", 3600),
             float("inf"): ("day", 86400)}

    seconds_difference = time1 - time2
    type_conversion = float if accurate else int
    format_string = "{}".format("{:.1f} {}" if accurate else "{} {}")

    for unit_threshold, (unit_string, seconds_to_unit) in units.items():
        if seconds_difference <= unit_threshold:
            unit_difference = type_conversion(seconds_difference / seconds_to_unit)
            return format_string.format(unit_difference, unit_string) + ("" if unit_difference <= 1 else "s")

    raise ValueError(f"Input time is invalid '{time1}' and '{time2}', cannot parse.")


def get_abs_time_difference(time1, time2, accurate=True):
    return get_time_difference(max(time1, time2), min(time1, time2), accurate)
