#!/usr/bin/env python

import argparse
import json

import requests


def main(options):

    r = requests.get(options.url)
    if not r.ok:
        print "Cannot load url: error %d, response: %s" % (r.status_code, r.content[:100])
        return


    db_info = r.json()

    print "Database name: %s" % db_info['db_name']
    print "Deleted docs count: %d" % (db_info['doc_del_count'])

    if not db_info['doc_del_count']:
        print "Nothing to do here, exiting"
        return

    url = options.url
    if not url.endswith('/'):
        url += '/'

    print "Loading first block of changes"
    changes = requests.get(url + '_changes', params={'limit': 10000}).json()

    deleted = []

    purged = 0
    total = 0

    i = 0
    while changes['results']:
        deleted.extend([(row['id'], [row['changes'][0]['rev']]) for row in changes['results'] if row.get('deleted')])


        if len(deleted) > 1000:
            r = requests.post(url + '_purge', data=json.dumps(dict(deleted)), headers={"Content-Type": "application/json"})
            if not r.ok:
                print "Error purging docs, code: %d, response: %s" % (r.status_code, r.content)
                break
            else:
                purged += len(deleted)

            print "Purged"
            deleted = []

        total += len(changes['results'])



        i += 1

        if not i % 10:
            print "%d processed, %d purged" % (total, purged)

        print "Loading next block from seq %d" % (changes['last_seq'])
        changes = requests.get(url + '_changes', params={'limit': 10000, 'since': changes['last_seq']}).json()

    if len(deleted):
        print "Purging last block (%d) of docs" % (len(deleted))
        r = requests.post(url + '_purge', data=json.dumps(dict(deleted)), headers={"Content-Type": "application/json"})
        if not r.ok:
            print "Error purging docs, code: %d, response: %s" % (r.status_code, r.content)
        else:
            purged += len(deleted)


    print "%d processed, %d purged" % (total, purged)
    print "All done, exiting"

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Purge deleted docs from database')
    parser.add_argument('url', help="Resource URL for database (like http://user:pass@example.com:5984/database_to_purge)")



    main(parser.parse_args())
