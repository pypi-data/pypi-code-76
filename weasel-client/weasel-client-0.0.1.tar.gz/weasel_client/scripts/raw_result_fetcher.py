import argparse
import datetime
import os
import sys

from weasel_client.raw_results.fetcher import ResultClient


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


parser = argparse.ArgumentParser(
    description='Fetches RAW website scans and translates their pseudonyms back to cleartext domains and urls.')
parser.add_argument('--pseudonyms', type=str, help='Path to a pseudonym database file.')
parser.add_argument('--date-from', type=valid_date)
parser.add_argument('--date-to', type=valid_date)
parser.add_argument('--server', type=str, default='https://weasel.cs.uni-bonn.de/polecat/')
parser.add_argument('--storage', type=str, help='Path to a directory to store downloaded files.')
parser.add_argument('--download-only', action='store_true')
args = parser.parse_args()

if __name__ == '__main__':
    if args.download_only and args.storage is None:
        print('Storage path need to be defined if using download-only mode.')
        exit(-1)

    # Create client connection and list available dates
    client = ResultClient(args.server, args.storage, args.pseudonyms)

    qs = client.results
    if args.date_from:
        qs = qs.range_from(args.date_from.year, args.date_from.month, args.date_from.day)

    if args.date_to:
        qs = qs.range_to(args.date_to.year, args.date_to.month, args.date_to.day)

    # Iterate over a RangeSet
    for results in qs:
        if args.download_only:
            results.download()
            print('Downloaded {}-{}-{}'.format(results.year, results.month, results.day))
            continue

        # Iter over day results
        for match in results.iter(stream=args.storage is None):
            # Only return result of which we know the cleartext
            if match.url is not None and match.domain is not None:
                raw = match.raw
                raw['cleartext_url'] = match.url
                raw['cleartext_domain'] = match.domain
                print(raw)
