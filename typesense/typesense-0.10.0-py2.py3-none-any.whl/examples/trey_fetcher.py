import requests
from bs4 import BeautifulSoup as Soup
import json
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}

with open('/tmp/trey.jsonl', 'w') as outfile:
    page = 1

    documents = []

    while page <= 16:
        url = 'https://qtg5aekc2iosjh93p.a1.typesense.net/collections/s/documents/search?query_by=title,primary_artist_name,album_name&q=trey+songz+slow+motion&filter_by=&max_facet_values=20&page=1&x-typesense-api-key=8hLCPSQTYcBuK29zY5q6Xhin7ONxHy99&num_typos=0&include_fields=id,release_date,title,primary_artist_name,album_name&max_hits=all&per_page=250&page='+str(page)

        body = requests.get(url, headers=HEADERS).content
        res = json.loads(body)

        for hit in res['hits']:
            hit['document']['id_int'] = int(hit['document']['id'])
            documents.append(hit['document'])

        page += 1
        time.sleep(1)

    documents.sort(key=lambda x: x['id_int'])

    for document in documents:
        outfile.write(json.dumps(document) + '\n')

