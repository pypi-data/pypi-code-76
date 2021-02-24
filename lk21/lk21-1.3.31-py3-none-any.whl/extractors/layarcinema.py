from . import Base


class layarcinema():
    tag = None
    host = "http://213.166.69.166"

    def extract(self, id):
        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        self._write(soup)

    def search(self, query, page=1):
        raw = self.session.get(f"{self.host}/page/{page}",
                               params={"s": query})
        soup = self.soup(raw)

        for item in soup.findAll(class_="ml-item"):
            a = item.find("a")
            r = {
                "id": self.getPath(a.attrs["href"]),
                "title": a.attrs["title"]
            }

            for k in ("mli-quality", "mli-rating", "mli-durasi"):
                if (i := item.find(class_=k)) and i.text:
                    r[k] = i.text
            yield r
