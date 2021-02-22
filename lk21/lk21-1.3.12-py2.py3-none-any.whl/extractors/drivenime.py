from . import Base


class drivenime(Base):
    tag = "anime"
    host = "https://drivenime.com"

    def extract(self, id):
        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        dl = soup.find(class_="post-single-content")
        for p in dl.findAll("p"):
            if (p.find("a")) and "download" in p.text.lower():
                break
        title = self.re.findall(r"(?s)a>\s*(\[[^>]+?\])\s*<", str(p))
        return {
            ttl: a.attrs["href"] for ttl, a in zip(title, p.findAll("a"))
        }

    def search(self, query, page=1):
        raw = self.session.get(f"{self.host}/page/{page}", params={
            "s": query})
        soup = self.soup(raw)

        for post in soup.findAll(class_="post"):
            a = post.find("a")
            result = {
                "title": a.attrs["title"],
                "id": self.getPath(a.attrs["href"])
            }

            if (genre := post.find(class_="theauthor")):
                result["genre"] = [a.text for a in genre.findAll("a")]

            yield result
