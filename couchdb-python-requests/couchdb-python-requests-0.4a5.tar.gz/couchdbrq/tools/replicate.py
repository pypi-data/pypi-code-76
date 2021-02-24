#!/usr/bin/env python

import time
import logging
import argparse
import json

import requests

## from couchdbrq import Server


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('replicate')
logger.setLevel(logging.DEBUG)





class Replicator(object):

    def __init__(self, options):

        self.options = options
        print self.options

        self.source = options.source
        self.target = options.target

        ## server1, nop, db1 = options.source.rpartition('/')

        ## self.source_server = Server(server1)
        ## self.source_db = self.source_server[db1]

        ## server2, nop, db2 = options.target.rpartition('/')

        ## self.target_server = Server(server2)
        ## self.target_db = self.target_server[db2]



    def run(self):

        ## logger.warning("Source: %s" % self.source_db.info())
        ## logger.warning("Target: %s" % self.target_db.info())

        seq = 0

        while True:

            logger.info("Loading changes from source, from seq %d", seq)
            r = requests.get(
                '%s/_changes' % self.source,
                params={
                    'limit': 100,
                    'include_docs': 'true',
                    'since': seq,
                    'attachments': 'true',
                },
                timeout=30,
            )

            if r.ok:
                logger.debug("Response length: %.1f kbytes", len(r.content) / 1024.)
                data = r.json()

                logger.debug("%d items changed", len(data['results']))

                bulk = {}
                for row in data['results']:
                    # overwrite if duplicate, with latest rev
                    if row.get('doc'):
                        bulk[row['doc']['_id']] = row['doc']

                if bulk:
                    logger.debug("Performing bulk store of %d records", len(bulk))

                    r2 = requests.post(
                        '%s/_bulk_docs' % self.target,
                        data=json.dumps({
                            'new_edits': False,
                            'docs': bulk.values(),
                        }),
                        headers={
                            'Content-Type': 'application/json'
                        },
                        timeout=1800)

                    #r2 = self.target_db.update(bulk.values(), new_edits=False)
                    logger.debug("Done. Response: %s - %s", r2.status_code, r2.content)

                    if not r2.ok:
                        logger.critical("Error posting changes to target DB. Sleeping 5s and retrying")
                        time.sleep(5)
                        continue



                if data['last_seq'] != seq:
                    logger.debug("Moving to next seq %d", data['last_seq'])
                    seq = data['last_seq']
                else:
                    if self.options.one_shot:
                        logger.info("One shot in action. Exiting")
                        break
                    else:
                        logger.debug("No changes in source. Sleeping")
                        time.sleep(1)

            else:
                logger.error("Error fetching changes. Sleeping 5s and retrying")
                time.sleep(5)

        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Start replication between couchdb databases (as external process).
This is not internal CouchDB replication starter. It's external program, similar to CouchDB's replicator.


""")
    parser.add_argument('source', help="Resource URL for source database (like http://user:pass@example.com:5984/source_db)")
    parser.add_argument('target', help="Resource URL for target database (like http://user:pass@example.com:5984/source_db)")

    parser.add_argument('--one-shot', action='store_true', help="Exif after complete replication")


    logger.info('Starting')

    replicator = Replicator(parser.parse_args())
    replicator.run()
