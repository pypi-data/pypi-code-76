from . import Base


class anibatch(Base):
    tag = "anime"
    host = "https://o.anibatch.me/"

    def extract(self, id):
        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        dlx = soup.find(class_="dlx")
        result = {}
        for table in dlx.findAll("table"):
            d = {}
            for a in table.findAll("a"):
                d[a.text] = a.attrs["href"]
            strong = table.find("strong").text
            result[strong] = d
        return result

    def search(self, query, page=1):
        raw = self.session.get(f"{self.host}/page/{page}", params={
            "s": query})
        soup = self.soup(raw)

        for artikel in soup.findAll("article"):
            a = artikel.find("a")
            yield {
                "title": a.attrs["title"],
                "id": self.getPath(a.attrs["href"])
            }
