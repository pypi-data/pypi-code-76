from . import Base


class nekonime(Base):
    host = "https://nekonime.stream"
    tag = "anime"

    def extract(self, id, rextract=False):
        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        if (eps := soup.find(class_="daftarepi")):
            d = {}
            for a in eps.findAll("a"):
                d[a.text] = self.getPath(a.attrs["href"])
            key = self.choice(d.keys())
            return self.extract(d[key], rextract=True)

        elif not rextract and (eps := soup.find(class_="flircontainer")):
            for a in eps.findAll("a"):
                if "All Eps" == a.text:
                    ch = self.choice(["Lanjut", a.text])
                    if ch != "Lanjut":
                        return self.extract(self.getPath(a.attrs["href"]))
        if (ddl := soup.find(class_="soraddl")):
            d = {}
            for p in ddl.findAll(class_="soraurl"):
                result = {}
                for a in p.findAll("a"):
                    result[a.text] = a.attrs["href"]
                d[p.strong.text] = result
            return d

    def search(self, query, page=1):
        raw = self.session.get(f"{self.host}/page/{page}", params={"s": query})
        soup = self.soup(raw)

        for article in soup.findAll(class_="article-body"):
            a = article.find("a")
            yield {
                "title": a.text,
                "id": self.getPath(a.attrs["href"])
            }
