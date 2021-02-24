import requests
import bs4
import re
import PyInquirer
import sys
from urllib.parse import urlparse


class Base(object):
    def __init__(self, logging=None, args=None):
        self.session = self._build_session()
        self.re = re
        self.logging = logging
        self.printInfo = args.info if args else None
        self.counter = 0

    def _build_session(self) -> requests.Session:
        session = requests.Session()
        session.headers[
            "User-Agent"] = "Mozilla/5.0 (Linux; Android 7.0; 5060 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36"
        return session

    def soup(self, raw):
        text = raw.text if hasattr(raw, "text") else raw
        return bs4.BeautifulSoup(text, "html.parser")

    def getPath(self, url):
        return urlparse(url).path.strip("/")

    def _write(self, soup, file="x.html"):
        if hasattr(soup, "prettify"):
            soup = soup.prettify()
        with open(file, "wb") as f:
            f.write(soup.encode())

    def _reformat(self, raw):
        if not isinstance(raw, str) or re.match(r"^\d+\.", raw):
            return raw
        else:
            self.counter += 1
            raw = re.sub(r"^\s+|\s+$", "", raw)
            return f"{self.counter}. {raw}"

    def info(self, *args, **kwargs):
        if self.printInfo:
            self.logging.info(*args, **kwargs)

    def choice(self, choices, msg=None, reset_counter=True):
        if reset_counter:
            self.counter = 0
        choices = list(choices)
        if len(choices) == 0:
            sys.exit("pilihan kosong")

        if len(choices) == 1:
            return choices[0]

        nch = {
            self._reformat(v): v for v in choices}
        questions = [
            {
                "type": "list",
                "name": "js",
                "message": msg or "pilih:",
                "choices": list(nch.keys())
            }
        ]

        output = PyInquirer.prompt(questions).get("js", "")
        return re.sub(r" \(direct\)$", "", nch[output])
