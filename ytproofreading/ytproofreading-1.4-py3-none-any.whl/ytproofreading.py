"""
Copyright (c) 2021 6ast1an979
This software is released under the MIT License, see LICENSE.
"""

import requests
import urllib.parse
from bs4 import BeautifulSoup

url = "https://jlp.yahooapis.jp/KouseiService/V1/kousei"


class Kousei(object):

    def __init__(self, appid):
        self.appid = appid

    def proofreading_support(self, sentence, filter_group=None, no_filter=None):
        """
        Proofread the text.

        Parameters
        ----------
        sentence : str
            Text to be proofread.
        filter_group : int
            Specify the number of the pointing group.
        no_filter : int
            Specify the remarks to be excluded from the remarks group.
        """

        result = []

        payload = {"appid": self.appid, "sentence": sentence}

        pointinggroup = list(range(1, 5))

        if filter_group in pointinggroup:
            payload["filter_group"] = str(filter_group)
        else:
            filter_group = ""

        identificationnumber = list(range(1, 18))

        if no_filter in identificationnumber:
            payload["no_filter"] = str(no_filter)
        else:
            no_filter = ""

        response = requests.get(url, params=payload)

        soup = BeautifulSoup(response.text, "lxml")

        if soup.find("error") is None:
            pass
        else:
            error_message = soup.find("error").find("message").get_text()
            raise RuntimeError(
                error_message.replace('\n', '') +
                "\nPlease check the error code." +
                "https://developer.yahoo.co.jp/appendix/errors.html"
            )

        startpos = soup.find_all("startpos")
        lengths = soup.find_all("length")
        surfaces = soup.find_all("surface")
        shitekiwords = soup.find_all("shitekiword")
        shitekiinfos = soup.find_all("shitekiinfo")

        fields = zip(startpos, lengths, surfaces, shitekiwords, shitekiinfos)

        for startpos, length, surface, shitekiword, shitekiinfo in fields:
            result.append({
                "startpos": startpos.get_text(),
                "length": length.get_text(),
                "surface": surface.get_text(),
                "shitekiword": shitekiword.get_text(),
                "shitekiinfo": shitekiinfo.get_text(),
            })

        return result