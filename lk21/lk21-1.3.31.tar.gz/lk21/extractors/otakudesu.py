from . import Base


class otakudesu(Base):
    tag = "anime"
    host = "https://otakudesu.tv"

    def extract(self, id):
        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        if (eps := soup.findAll(class_="episodelist")[1:]):
            ch = {}
            for li in eps[0].findAll("li"):
                ch[li.a.text] = li.a.attrs["href"]
            id = self.choice(ch.keys())
            return self.extract(self.getPath(ch[id]))
        else:
            dls = {}
            for dl in soup.findAll("div", class_="download"):
                title = [h4.text for h4 in dl.findAll("h4")]
                for n, ul in enumerate(dl.findAll("ul")):
                    if len(title) == 1:
                        n = 0
                    n = title[n]
                    if not dls.get(n):
                        dls[n] = {}
                    for li in ul.findAll("li"):
                        dls[n][f"{li.strong.text}/{li.i.text}"] = {
                            a.text: a.attrs["href"] for a in li.findAll("a")
                        }
            key = self.choice(dls.keys())
            return dls[key]

    def search(self, query, page=1):
        raw = self.session.get(self.host, params={
            "s": query, "post_type": "Anime"})
        soup = self.soup(raw)

        ul = soup.find("ul", class_="chivsrc")
        for li in ul.findAll("li"):
            result = {
                "title": li.a.text,
                "id": self.getPath(li.a.attrs["title"])
            }
            yield result
