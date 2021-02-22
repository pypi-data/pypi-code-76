from . import Base


class samehadaku(Base):
    tag = "anime"
    host = "https://samehadaku.vip"

    def extract(self, id):
        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        if id.startswith("anime/"):
            ch = {}
            if (listeps := soup.findAll(class_="epsleft")):
                for li in listeps:
                    a = li.find("a")
                    ch[a.text] = self.getPath(a.attrs["href"])
            if (batch := soup.find(class_="listbatch")):
                ch[batch.text] = self.getPath(batch.a.attrs["href"])
            key = self.choice(ch)
            return self.extract(ch[key])

        result = {}
        for dl in soup.findAll(class_="download-eps"):
            d = {}
            for li in dl.findAll("li"):
                item = {}
                for a in li.findAll("a"):
                    item[a.text] = a.attrs["href"]
                d[li.strong.text] = item
            result[dl.p.text] = d
        return result

    def search(self, query, page=1):
        raw = self.session.get(f"{self.host}/page/{page}", params={
            "s": query})
        soup = self.soup(raw)

        for article in soup.findAll("article", class_="animpost"):
            result = {
                "id": self.getPath(article.find("a").attrs["href"])
            }

            for k in ("score", "title", "type", "genres"):
                if (v := article.find(class_=k)):
                    name = " ".join(v.attrs["class"])
                    if (aa := v.findAll("a")):
                        result[name] = [a.text for a in aa]
                    elif v.text:
                        result[name] = v.text
            yield result
