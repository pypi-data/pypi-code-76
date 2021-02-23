#!/usr/bin/env python

from time import time, sleep
import argparse
from datetime import datetime, timedelta, date
import sys
import socket

from sicor.ECMWF import download_variables
from sicor.ECMWF.ECMWF import test


# noinspection PyProtectedMember
def get_lock(process_name):
    # Without holding a reference to our socket somewhere it gets garbage
    # collected when the function exits
    get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    try:
        get_lock._lock_socket.bind('\0' + process_name)
    except socket.error:
        print('lock exists -> exit here')
        sys.exit()


def countdown(execute_every, print_update=timedelta(seconds=1), tsleep=1):
    assert execute_every > print_update
    assert isinstance(execute_every, timedelta)
    assert isinstance(print_update, timedelta)
    t0, t1 = datetime.now(), datetime.now()
    while True:
        sleep(tsleep)
        if datetime.now() - t0 > execute_every:
            break
        if datetime.now() - t1 > print_update:
            td = (t0+execute_every-datetime.now())
            hh, rem = divmod(td.total_seconds(), 3600)
            mm, ss = divmod(rem, 60)
            print(datetime.now().strftime('%Y/%m/%d %H:%M:%S'), "-- next in --> %ih:%im:%ss" % (hh, mm, int(ss)))
            t1 = datetime.now()


def sicor_ecmwf_parser():
    """Return parser for sicor_ecmwf.py script."""

    default_products = [
        "fc_T2M",
        "fc_O3",
        "fc_SLP",
        "fc_TCWV",
        "fc_GMES_ozone",
        "fc_total_AOT_550nm",
        "fc_sulphate_AOT_550nm",
        "fc_black_carbon_AOT_550nm",
        "fc_dust_AOT_550nm",
        "fc_organic_matter_AOT_550nm",
        "fc_sea_salt_AOT_550nm"]

    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", default=False, help="Run Test downloads.")
    parser.add_argument("-p", "--db_path", action="store", type=str, default="./db_ECMWF/",
                        help="Root path do database which will be created.")
    parser.add_argument("-f", "--date_from", action="store", type=str, default="2016/01/01",
                        help="Start date in format: YYYY/MM/DD")
    parser.add_argument("-t", "--date_to", action="store", type=str, default="today",
                        help="To date in format: YYYY/MM/DD")
    parser.add_argument("-d", "--days", action="store", type=int, default=0,
                        help="Download data for last [Days], ignoring -f and -t.")
    parser.add_argument("-r", "--repeat", action="store", type=str, default="1/0/0",
                        help=(
                            "Repeat [repeat]/[repeat every hour fraction]/[print status every seconds], e.g. 2/0.5/30, "
                            "[repeat]=0 repeats forever "
                        ))
    parser.add_argument("-i", "--processes", action="store", type=int, default=0)
    parser.add_argument("-v", "--variables", action="store", type=str,
                        default=",".join(default_products), help="Comma separated list of to be retrieved variables.")
    parser.add_argument("-F", "--force", action="store_true", default=False, help="Force downloads.")
    parser.add_argument("-m", "--max_step", action="store", type=int, default=120,
                        help="Maximum forecast step to download.")
    return parser


if __name__ == "__main__":

    parser = sicor_ecmwf_parser()
    args = parser.parse_args()

    if args.test is True:
        test()
        exit()

    variables = args.variables.split(",")

    repeats, houres_wait, seconds_update = [float(jj) for jj in args.repeat.split("/")]
    ii = 0
    while True:
        ii += 1

        if args.days == 0:
            if args.date_to == "today":
                date_to = date.today()
            else:
                date_to = datetime.strptime(args.date_to, "%Y/%m/%d").date()

            if args.date_from == "today":
                date_from = date.today()
            else:
                date_from = datetime.strptime(args.date_from, "%Y/%m/%d").date()
        else:
            print("days option is set -> ignoring -f and -t option")
            date_to = datetime.now()
            date_from = date_to - timedelta(days=args.days)

        # avoid that this script runs with multiple instances -> try to get lock
        get_lock("ECMWF")
        print("From:%s" % str(date_from))
        print("To:%s" % str(date_to))
        print("DB path: %s" % str(args.db_path))
        print("Variables: %s" % str(variables))

        try:
            t0 = time()
            results = download_variables(date_from=date_from, date_to=date_to, db_path=args.db_path,
                                         max_step=args.max_step, ecmwf_variables=variables, processes=args.processes,
                                         force=args.force)
            t1 = time()
            print("Runtime: %.2f" % (t1 - t0))
            for result in results:
                print(result)

        except Exception as err:
            print("Exception occurred.")
            print(repr(err))

        if ii < repeats or repeats == 0:
            countdown(timedelta(hours=houres_wait), print_update=timedelta(seconds=seconds_update))
        else:
            break


