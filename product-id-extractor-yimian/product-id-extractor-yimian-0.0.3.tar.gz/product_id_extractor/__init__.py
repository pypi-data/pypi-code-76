import re
from urllib.parse import urlparse

from product_id_extractor.config import Config

rules = Config.RULES


class Extractor:
    def __init__(self, url, platform=''):
        self.url = self.url_validate(url)
        self.platform = platform.lower()

    def url_validate(self, url):
        regex = re.compile(
            r"^https?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        if url is None or not regex.search(url):
            raise Exception("Invalid URL")
        return url

    def extract(self):
        if not self.url:
            return None
        if not self.platform:
            return self.auto_extractor()
        elif self.platform in Config.RULES:
            return self.platform_extractor()
        else:
            return None

    # def tmall_extractor(self):
    #     reg = re.search(rules["tmall"], self.url)
    #     return reg.group(1) if reg.group(1) else None

    # def taobao_extractor(self):
    #     reg = re.search(rules["taobao"], self.url)
    #     return reg.group(1) if reg.group(1) else None

    # def jd_extractor(self):
    #     reg = re.search(rules["jd"], self.url)
    #     return reg.group(1) if reg.group(1) else None

    # def suning_extractor(self):
    #     reg = re.search(rules["suning"], self.url)
    #     return reg.group(1) if reg.group(1) else None

    # def amazon_extractor(self):
    #     reg = re.search(rules["amazon"], self.url)
    #     return reg.group(1) if reg.group(1) else None
    def platform_extractor(self):
        reg = re.search(rules[self.platform], self.url)
        return reg.group(1) if reg else None

    def auto_extractor(self):
        for v in rules.values():
            reg = re.search(v, self.url)
            if reg:
                return reg.group(1)
        return None
