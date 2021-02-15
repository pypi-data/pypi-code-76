################################################################
# pp.client - Produce & Publish Python Client
# (C) 2013, ZOPYX Ltd, Tuebingen, Germany
################################################################

from __future__ import print_function

import plac
import base64
import json
import time
import pprint
import requests

@plac.annotations(
    server_url=('URL of Produce & Publish API)', 'option', 's'),
)
def available_converters(server_url='http://localhost:6543'):
    if server_url.endswith('/'):
        server_url = server_url[:-1]
    result = requests.get(server_url + '/converters')
    if result.status_code == 200:
        pprint.pprint(result.json())
    else:
        print(result)


def main():
    plac.call(available_converters)

if __name__ == '__main__':
    main()
