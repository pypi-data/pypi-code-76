from . import Base


class riie(Base):
    tag = "anime"
    host = "https://riie.jp"

    def extract(self, id):
        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        self._write(soup)

        if (eps := soup.findAll(id="episodes-list")):
            lst = {}
            for ep in eps:
                if (items := ep.findAll("li", class_="ep-item")):
                    title = ep.find(class_="gh-title").text

                    raw = {}
                    for item in items:
                        a = item.find("a")
                        if "download" in title.lower():
                            raw[a.text] = a.attrs["href"]
                        else:
                            raw[a.text] = "re:" + self.getPath(a.attrs["href"])
                    lst[title] = raw
            return lst

    def search(self, query, page=1):
        raw = self.session.get(f"{self.host}/search/{page}/{query}")
        soup = self.soup(raw)

        if (result := soup.find(class_="filter-result")):
            self._write(soup)
            for ul in result.findAll("ul"):
                for li in ul.findAll("li"):
                    a = li.find(class_="item-title").a
                    r = {
                        "id": self.getPath(a.attrs["href"]),
                        "title": a.text
                    }
                    for kl in ("tv-type", "gr-eps", "gr-type", "gr-sub"):
                        if (it := li.find(class_=kl)):
                            r[kl] = it.text
                    yield r
