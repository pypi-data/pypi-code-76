
import time
import sys
import random
import json

import requests

def main(doc_id):


    i = 0
    time_max = 0
    db_key = random.choice(['smscoin_cluster', 'smscoin_cluster2', 'smscoin_cluster3'])
    print db_key

    #s = requests.Session()
    s = requests
        
    
    while True:
        doc = s.get('http://smscoin:Poh0saece5no@localhost:5984/%s/%s' % (db_key, doc_id)).json()
        doc['position'] += 1
        doc['status'] = 'rev %s reached' % doc['_rev']
        
        start = time.time()

        s.put('http://smscoin:Poh0saece5no@localhost:5984/%s/%s' % (db_key, doc_id), data=json.dumps(doc))
        
        lost = time.time() - start

        if lost > time_max:
            time_max = lost

        if not i % 100:
            print time.time(), i, time_max, doc['_rev']

        i += 1
        
        
    pass


if __name__ == '__main__':
    main(sys.argv[1])

    
