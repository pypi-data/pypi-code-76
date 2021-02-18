#!/usr/bin/env python3
import argparse
import datetime
import json
import logging
import time

from . import Whatsapp

def json_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

parser = argparse.ArgumentParser()
parser.add_argument("--geckopath", help="Path to your gecko driver (necessary if not in $PATH)")
parser.add_argument("--output", help="File to store the output", default="output.json")
parser.add_argument("--blur", action="store_true")
parser.add_argument("--verbose", "-v", help="Verbose (debug) output", action="store_true", default=False)

args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                    format='[%(asctime)s %(name)-12s %(levelname)-5s] %(message)s')

#Get website, allow 15 seconds to scan the QR code
myscraper = Whatsapp(geckopath=args.geckopath)
try:
    time.sleep(15)
    if args.blur:
        myscraper.blur()
    with open(args.output, 'w') as fout:
        for i, chatlinks in enumerate(myscraper.scrape_links()):
            logging.info(f"Scraped links from chat number {i}...")
            fout.write(json.dumps(chatlinks, default = json_converter))
            fout.write('\n')
    logging.info(f"Done. All links saved to {args.output}")
finally:
    myscraper.quit_browser()


