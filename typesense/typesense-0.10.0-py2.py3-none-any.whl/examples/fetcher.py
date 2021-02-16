import requests
from bs4 import BeautifulSoup as Soup
import json
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}

REC_SELECTOR = 'h3[data-scp=inline_recirc_headline] a'
REC_SELECTOR2 = 'aside[data-scp=related_content] h3 a'

with open('/Users/kishore/others/wreally/recodemo/wirecutter_recos2.jsonl', 'w') as outfile:
    with open('/Users/kishore/others/wreally/recodemo/wirecutter.txt') as infile:
        for url in infile:
            html = requests.get(url, headers=HEADERS).content
            soup = Soup(html, features="lxml")
            title = soup.select_one('meta[property="og:title"]').attrs['content']
            desc = soup.select_one('meta[property="og:description"]').attrs['content']

            page = {}
            page['title'] = title
            page['desc'] = desc

            recs = soup.select(REC_SELECTOR)
            if not recs:
                recs = soup.select(REC_SELECTOR2)

            page['recos'] = []

            for rec in recs:
                reco = {'title': rec.text, 'url': rec.attrs['href']}
                page['recos'].append(reco)

            outfile.write(json.dumps(page) + '\n')
            print(title)

            time.sleep(0.3)

