from . import Base


class anikyojin(Base):
    host = "https://anikyojin.net"
    tag = "anime"

    def extract(self, id):
        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        result = {}
        for dc in soup.findAll(class_="downloadcloud"):
            reso = {}
            for li in dc.findAll("li"):
                d = {}
                for a in li.findAll("a"):
                    d[a.text] = a.attrs["href"]
                reso[li.strong.text] = d
            result[dc.h2.text] = reso
        return result

    def search(self, query, page=1):
        raw = self.session.get(f"{self.host}/page/{page}", params={
            "s": query, "post_type": "post"})
        soup = self.soup(raw)

        for article in soup.findAll(class_="artikel"):
            a = article.h2.find("a")

            result = {
                "title": a.text,
                "id": self.getPath(a.attrs["href"])
            }

            for li in article.find(class_="info").findAll("li"):
                k, v = self.re.split(r"\s*:\s*", li.text)
                if "," in v:
                    v = self.re.split(r"\s*,\s*", v)
                result[k] = v

            yield result
