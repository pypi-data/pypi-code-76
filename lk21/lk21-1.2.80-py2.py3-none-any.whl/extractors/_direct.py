from . import Base

class _direct(Base):
    """
    Extractor
    """
    def extract_direct_url(self, url):
        for title, pattern in self.directRules.items():
            if pattern.match(url):
                self.logging.info(f"Mengekstrak {title[1:]}: {url}")
                func = getattr(self, title)
                result = func(url)

                key = self.choice(result.keys())
                return result[key]
        return url

    def _zippyshare(self, url):
        raw = self.session.get(url)
        res = self.re.search(
            r'href = "(?P<i>[^"]+)" \+ \((?P<t>[^>]+?)\) \+ "(?P<f>[^"]+)', raw.text)
        if res is not None:
            res = res.groupdict()
            return {
                "": self.re.search(r"(^https://www\d+.zippyshare.com)", raw.url).group(1) +
                res["i"] + str(eval(res["t"])) + res["f"]}
        return {"": url}

    def _fembed(self, url):
        raw = self.session.get(url)
        api = self.re.search(r"(/api/source/[^\"']+)", raw.text)
        if api is not None:
            result = {}
            raw = self.session.post(
                "https://layarkacaxxi.icu" + api.group(1)).json()
            for d in raw["data"]:
                f = d["file"]
                direct = self.session.head(f).headers.get("Location", f)
                result[f"{d['label']}/{d['type']}"] = direct
            return result
