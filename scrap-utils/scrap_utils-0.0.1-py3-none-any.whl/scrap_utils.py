"""This module provides some functions that might save you from repetition in scraping projects."""
import csv, json, math, time
import requests


class MaxTryReached(Exception):
    """Error when max trial has been reached"""
    pass


def load_json(filepath, encoding=None, errors=None, parse_float=None,
        parse_int=None, parse_constant=None):
    """Load json from file."""
    with open(filepath, 'r', encoding=encoding, errors=errors) as file:
        data = json.load(file, parse_float=parse_float, parse_int=parse_int,
                        parse_constant=parse_constant)
    print("Json loaded from", filepath)
    return data


def dump_json(data, filepath, encoding=None, errors=None, indent=4,
        skipkeys=False, ensure_ascii=False, separators=None, sort_keys=False):
    """Dump json data into filepath."""
    with open(filepath, 'w', encoding=encoding, errors=errors) as file:
        json.dump(
            data, file, indent=indent, skipkeys=skipkeys,
            ensure_ascii=ensure_ascii, separators=separators,
            sort_keys=sort_keys
        )
    print("Json dumped to", filepath)


def to_csv(dataset, filepath, mode="a", encoding=None, errors=None, newline='',
        header=True, dialect='excel', **fmtparams):
    """Save dataset to csv file."""
    with open(filepath, mode=mode, encoding=encoding, errors=errors,
            newline=newline) as csvfile:
        writer = csv.writer(csvfile, dialect=dialect, **fmtparams)
        if header:
            writer.writerows(dataset)
        else:
            writer.writerows(dataset[1:])
    print("Dataset saved to", filepath)


def requests_get(url, trials=0, sleep_time=30, max_try=math.inf, **requests_kwargs):
    """Send a get request with requests library. 
    Keep retrying till max_try when there's a bad code or error.
    """
    trials += 1

    try:
        response = requests.get(url, **requests_kwargs)
        if response.status_code == 200:
            return response
        else:
            print("\nRequests Get Bad Status Code: {}\nTrial: {}; Max Try: {}; Sleep Time: {}\nUrl: {}\n".format(
                response.status_code, trials, max_try, sleep_time, url)
            )
    except Exception as e:
        print("\nRequests Get Error: {}\nTrial: {}; Max Try: {}; Sleep Time: {}\nUrl: {}\n".format(
            e, trials, max_try, sleep_time, url)
        )

    # When there's error or bad status code.
    if trials < max_try:
        time.sleep(sleep_time)
        return requests_get(url, trials, sleep_time, max_try, **requests_kwargs)
    else:
        raise MaxTryReached("Max Trial of {} has been reached for requests get. Url: {}".format(max_try, url))


def requests_post(url, trials=0, sleep_time=30, max_try=math.inf, **requests_kwargs):
    """ Send a post request with requests library.
    Keep retrying till max_try when there's a bad code or error.
    """
    trials += 1

    try:
        response = requests.post(url, **requests_kwargs)
        if response.status_code == 200:
            return response
        else:
            print("\nRequests Post Bad Status Code: {}\nTrial: {}; Max Try: {}; Sleep Time: {}\nUrl: {}\n".format(
                response.status_code, trials, max_try, sleep_time, url)
            )
    except Exception as e:
        print("\nRequests Post Error: {}\nTrial: {}; Max Try: {}; Sleep Time: {}\nUrl: {}\n".format(
            e, trials, max_try, sleep_time, url)
        )

    # When there's error or bad status code.
    if trials < max_try:
        time.sleep(sleep_time)
        return requests_post(url, trials, sleep_time, max_try, **requests_kwargs)
    else:
        raise MaxTryReached("Max Trial of {} has been reached for requests post. Url: {}".format(max_try, url))
