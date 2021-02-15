from . import Base

class animeindo(Base):
    desc = "anime batch"
    host = "https://animeindo.asia"

    def extract(self, id):
        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        if (eps := soup.findAll(class_="episode_list")):
            d = {}
            for ep in eps:
                d[ep.a.text.split(" -")[0]] = self.getPath(ep.a.attrs["href"])
            key = self.choice(d.keys())
            return self.extract(d[key])

        stsoup = str(soup)
        formats = self.re.findall(r"(Format .+?)\s*:", stsoup)

        result = {fm: {} for fm in formats}
        k = 0
        for p in soup.findAll("p", class_="has-text-align-center"):
            if (aa := p.findAll("a")):
                info = [self.re.split(r"\s*:", i)[0] for i in 
                    self.re.findall(r">\s*(\d+p(?:\s+.+?)?)\s*:", str(p))]
                if len(info) == 1:
                    result[formats[k]][info[0]] = {
                        a.text: a.attrs["href"] for a in aa
                    }
                else:
                    # TODO: parse p yang ini
                    break
        return result

    def search(self, query, page=1):
        raw = self.session.get(f"{self.host}/page/{page}", params={
            "s": query})
        soup = self.soup(raw)

        for animposx in soup.findAll(class_="animposx"):
            a = animposx.find("a")
            yield {
                "title": a.attrs["title"],
                "id": self.getPath(a.attrs["href"])
            }
            break
