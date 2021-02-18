# hip.py

import re
import http.client
from typing import List, Dict


def get(method: str, url: str) -> List[Dict[str, str]]:
  """
  Fetch data from the url provided, returns the data.
  
  All arguments must be of equal length.
  :param method: the method of the request
  :param url: url to fetch from
  :return: data
  """

  if method == 'GET':
    # remove the http or https from the url
    stripped_url = re.sub(r'(http://|https://)', '', url)

    domiain_name =  stripped_url.partition('/')[0]
    end_point = stripped_url.partition('/')[-1]

    conn = http.client.HTTPSConnection(domiain_name)
    conn.request("GET", "/{}".format(end_point))

    r1 = conn.getresponse()
    data1 = r1.read()  # the fetched data

    return [{ 'status': r1.status, 'data': data1 }]
  return 'Only get request allowed'
