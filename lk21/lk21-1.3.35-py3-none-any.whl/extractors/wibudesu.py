from . import Base


class wibudesu(Base):
    host = "https://wibudesu.com"
    tag = "anime"

    def extract(self, id):
        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        lexot = soup.find(class_="lexot")

        result = {}
        for p in lexot.findAll("p")[1:]:
            if (links := p.findAll("a")):
                title = p.strong.text
                d = {}
                for a in links:
                    d[a.text] = a.attrs["href"]
                result[title] = d
        return result

    def search(self, query, page=1):
        raw = self.session.get(f"{self.host}/page/{page}", params={
            "s": query, "post_type": "post"})
        soup = self.soup(raw)

        for detpost in soup.findAll(class_="detpost"):
            a = detpost.find("a")
            result = {
                "title": a.attrs["title"],
                "id": self.getPath(a.attrs["href"])
            }

            if (morec := detpost.find(class_="morec")):
                result["genre"] = [a.text for a in morec.findAll("a")]

            yield result
