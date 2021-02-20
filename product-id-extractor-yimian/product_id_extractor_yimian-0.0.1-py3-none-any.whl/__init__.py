import re

from product_id_extractor.config import Config

rules = Config.RULES

class Extractor:

    def __init__(self, url, platform=None):
        self.url = url
        self.platform = platform

    def extract(self):
        if not self.url:
            return None
        if not self.platform:
            return self.auto_extractor()
        elif self.platform in ["tmall", "taobao"]:
            return self.tmall_taobao_extractor()
        elif self.platform in ["jd", "suning"]:
            return self.jd_suning_extractor()
        elif self.platform == "amazon":
            return self.amazon_extractor()


    def tmall_taobao_extractor(self):
        reg = re.search(rules["tmall_taobao"], self.url)
        return reg[0][3:] if reg else None


    def jd_suning_extractor(self):
        reg = re.search(rules["jd_suning"], self.url)
        tail_len = len(reg[0]) - 5
        return reg[0][:tail_len] if reg else None


    def amazon_extractor(self):
        reg = re.search(rules["amazon"], self.url)
        return reg[0][3:] if reg else None


    def auto_extractor(self):
        for k, v in rules.items():
            reg = re.search(v, self.url)
            if reg and (k in ["tmall_taobao", "amazon"]):
                return reg[0][3:]
            elif reg and (k == "jd_suning"):
                tail_len = len(reg[0]) - 5
                return reg[0][:tail_len]
        return None
