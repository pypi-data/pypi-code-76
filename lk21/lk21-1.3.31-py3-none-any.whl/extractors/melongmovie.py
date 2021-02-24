from . import Base


class melongmovie(Base):
    tag = "movie"
    host = "https://melongmovie.com"

    def extract(self, id):
        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        result = {}
        for ep in soup.findAll(text=self.re.compile(r"(?i)episode\s+\d+")):
            content = ep.findNext("div")

            r = {}
            for p in content.findAll("p"):
                if p.a:
                    y = {}
                    for a in p.findAll("a"):
                        y[a.text] = a["href"]
                    title = self.re.search(r"\s*([^=]+)", p.text)
                    r[title.group(1)] = y
            result[ep] = r

        pattern = self.re.compile(r"[A-Z ]+:")
        if (ref := soup.find("strong", text=pattern)):
            for li in ref.findAllNext("li"):
                sub = "/".join(strong.text for strong in li.findAll("strong"))

                r = {}
                for a in li.findAll("a"):
                    r[a.text] = a["href"]

                title = li.findPrevious(
                    "strong", text=pattern).text.strip(": \n")
                if not result.get(title):
                    result[title] = {}
                result[title][sub] = r

        return result

    def search(self, query, page=1):
        raw = self.session.get(f"{self.host}/page/{page}",
                               params={"s": query})
        soup = self.soup(raw)

        if (los := soup.find(class_="los")):
            for article in los.findAll("article"):
                a = article.find("a")
                r = {
                    "id": self.getPath(a.attrs["href"]),
                    "title": a.attrs["alt"]
                }

                for k in ("quality", "eps"):
                    if (i := article.find(class_=k)):
                        r[k] = i.text
                for ip in ("genre", "name"):
                    if (i := article.findAll(itemprop=ip)):
                        r[ip] = [a.text for a in i]
                yield r
