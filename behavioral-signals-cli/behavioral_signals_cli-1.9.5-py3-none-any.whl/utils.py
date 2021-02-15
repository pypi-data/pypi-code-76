#
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4:
#

# -- essential utils
import os
import sys
import csv
import logging
import pprint
from dateutil.parser import parse
from ruamel.yaml import YAML

from .settings import (NUM_PROCESSING_REQUIRED_METADATA,
                       REQUESTS_LIMIT_PERIOD_SECS,
                       MAX_REQUESTS_PER_SEC)


def readConf(file):
    """
    Read a yml dict
    """
    with open(file, "rb") as fp:
        d = fp.read()
        yaml = YAML(typ='safe')   # default, if not specfied, is 'rt' (round-trip)
        cdict = yaml.load(d)
        return cdict


def ppr(cdict):
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(cdict)


def ppf(cdict):
    pp = pprint.PrettyPrinter(indent=1)
    return pp.pformat(cdict)


def die(msg, exitCode=1):
    """
    Print a message and exit
    """
    progname = os.path.basename(sys.argv[0])
    sys.stderr.write(("{}: {}\n".format(progname, msg)))
    sys.exit(exitCode)


def words(file):
    """
    Generate all words in file
    """
    with open(file, 'r') as f:
        if os.stat((f.name)).st_size == 0:
            logging.error("Log file '{}' is empty".format(f.name))
        for line in f:
            if line.strip().isdigit():
                for word in line.split():
                    yield int(word.strip())
            else:
                logging.error("'{}' file should include only integer values. Value {} is not acceptable".format(f.name, line))
                continue


def getnpopn(lista, n):
    """
    Removes and returns the `n` first items on list `lista`
    """
    n = min(n, len(lista))

    items = lista[0:n]

    for i in range(n):
        lista.pop(0)

    return items


def convert_iso_datetime(calltime):
    """
    Convert datetime string to ISO datetime string
    """
    service_datetime_fmt = '%m/%d/%Y %H:%M:%S'

    if calltime is None:
        return calltime

    try:
        calltime = parse(calltime)
        calltime = calltime.strftime(service_datetime_fmt)
    except ValueError:
        return None
    else:
        return calltime


def max_timeout(size: int, kbps: int = 100):
    """
    Estimates the maximum time for a file to complete uploading
    """
    return int(size / (kbps * 1000 / 8))


def get_csv_non_empty_rows(csv_file):
    """
    Returns the number of `non empty` rows in CSV file
    """
    def valid_row(row):
        if len(row) < NUM_PROCESSING_REQUIRED_METADATA:
            return False

        for i in range(NUM_PROCESSING_REQUIRED_METADATA):
            if len(row[i].strip()) < 1:
                return False

        return True

    row_count = 0

    with open(csv_file, 'r') as f:
        reader = csv.reader(f, delimiter=",", quotechar="'")
        row_count = sum(1 for row in reader if valid_row(row))

    return row_count


def limit_upload_rate(uploads_history, t_last, n_last):
    N = 0

    uploads_history.append((t_last, n_last))

    (t_first, n_first) = uploads_history[0]

    for (t, n) in uploads_history:
        N += n

    if (N >= MAX_REQUESTS_PER_SEC) and (t_last - t_first < REQUESTS_LIMIT_PERIOD_SECS):
        return True

    elif (N >= MAX_REQUESTS_PER_SEC) and (t_last - t_first >= REQUESTS_LIMIT_PERIOD_SECS):
        for (t, _) in uploads_history:
            if t_last - t < REQUESTS_LIMIT_PERIOD_SECS:
                break

            uploads_history.pop(0)

        return True

    elif (N < MAX_REQUESTS_PER_SEC) and (t_last - t_first >= REQUESTS_LIMIT_PERIOD_SECS):
        for (t, _) in uploads_history:
            if t_last - t < REQUESTS_LIMIT_PERIOD_SECS:
                break

            uploads_history.pop(0)

        return False

    return False
